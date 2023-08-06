# This file is a part of thelatinlibrary
#
# Copyright (c) 2018 The thelatinlibrary Authors (see AUTHORS)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from html import unescape
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

from thelatinlibrary import settings
from .authors import Author
from .exceptions import NoAuthorException

_authors = []
_endpoint = "http://www.thelatinlibrary.com/"
_exceptions = ["christian.html", "classics.html", "index.html",
               "medieval.html", "misc.html", "neo.html", "readme.html"]


def get_author(url: str) -> Author:
    """
    Used to return an Author by passing
    an URL as an argument.
    
    Example:
        All authors are associated to a link, so it is easy to get an author
        using it.

        >>> import thelatinlibrary
        >>> caesar = thelatinlibrary.get_author("http://www.thelatinlibrary.com/caes.html")
        >>> caesar
        Author(link='http://www.thelatinlibrary.com/caes.html', name='Caesar')

    Args:
      url (str): The thelatinlibrary.com URL.

    Returns:
      Author: The Author object.
    """
    global _authors

    url = url.replace("https://", "http://")

    if not url.startswith(_endpoint):
        url = _endpoint + url

    if settings.save_on_methods:
        try:
            return next(filter(lambda writer: writer.link == url, _authors))
        except StopIteration:
            pass

    text = requests.get(url).text
    parser = BeautifulSoup(text, "html5lib")

    if '404' in parser.title.string:
        raise NoAuthorException("No author has been found on %s" % url)
    else:
        author = Author(link=url, name=parser.title.string.strip().rstrip())

        if settings.save_on_methods and author not in _authors:
            _authors.append(author)

        return author


def get_author_by_name(name: str) -> Author:
    """
    Used to return an Author by passing
    a name as an argument.

    Args:
        name (str): The Author name.

    Example:
        All authors are listed in thelatinlibrary.com index, so it is
        easy to get an author using it.

        >>> import thelatinlibrary
        >>> caesar = thelatinlibrary.get_author_by_name("caesar")
        >>> caesar
        Author(link='http://www.thelatinlibrary.com/caes.html', name='Caesar')

    Raises:
        NoAuthorException: If no author has been found.

    Returns:
        Author: The Author object.
    """
    if settings.save_on_methods:
        try:
            return next(filter(lambda writer: writer.name.lower() == name.lower(), _authors))
        except StopIteration:
            pass

    text = requests.get(_endpoint + "indices.html").text
    parser = BeautifulSoup(text, "html5lib")

    tables = parser.find_all("td")

    for table in tables:
        links = table.find_all("a")

        for link in links:
            if link['href'] not in _exceptions:
                if link.string.strip().rstrip().lower() == name.lower():
                    author = Author(name=unescape(link.string.strip().rstrip()), link=_endpoint + link['href'])

                    if settings.save_on_methods and author not in _authors:
                        _authors.append(author)

                    return author

    raise NoAuthorException("There's no %s in the thelatinlibrary.com index." % name)


def get_authors(reload: Optional[bool] = False) -> List[Author]:
    """
    Used to return a list of all the classic
    authors found on thelatinlibrary.com.

    Args:
        reload (Optional[bool]): If it should be ignored the already stored authors. (Default value = False)

    Example:
        There's thelatinlibrary.com index, the function just returns it.

        >>> import thelatinlibrary
        >>> authors = thelatinlibrary.get_authors()
        >>> authors
        [Author(link='http://www.thelatinlibrary.com/abel.historia.html', name='Abelard'), ...,
        Author(link='http://www.thelatinlibrary.com/waardenburg.html', name='Waardenburg')]


    Raises:
        NoAuthorException: If no author has been found.

    Returns:
        List[Author]: A list of all the class authors.
    """
    global _authors

    if settings.save and _authors and not reload:
        return _authors

    text = requests.get(_endpoint + "indices.html").text
    parser = BeautifulSoup(text, "html.parser")

    authors, books, tomes = [], [], []
    tables = parser.find_all("td")

    for table in tables:
        links = table.find_all("a")

        for link in links:
            if link['href'] not in _exceptions:
                authors.append(Author(name=unescape(link.string.strip().rstrip()), link=_endpoint + link['href']))

    if settings.save:
        _authors = authors

    return authors
