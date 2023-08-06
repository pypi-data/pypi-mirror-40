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
from typing import List

import requests
from bs4 import BeautifulSoup

from .authors import Author

_endpoint = "http://www.thelatinlibrary.com/"
_exceptions = ["classics.html", "index.html", "readme.html"]


def get_authors() -> List[Author]:
    """
    Used to return a list of all the classic
    authors found on thelatinlibrary.com.

    :return: A list of all the class authors.
    :rtype: List[Author]
    """
    text = requests.get(_endpoint + "indices.html").text
    parser = BeautifulSoup(text, "html.parser")

    authors, books, tomes = [], [], []
    tables = parser.find_all("td")

    for table in tables:
        links = table.find_all("a")

        for link in links:
            if link['href'] not in _exceptions:
                authors.append(Author(name=unescape(link.string.strip().rstrip()), link=_endpoint + link['href']))

    return authors
