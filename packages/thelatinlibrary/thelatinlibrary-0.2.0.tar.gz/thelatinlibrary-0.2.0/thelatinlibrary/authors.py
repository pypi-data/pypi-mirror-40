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

from dataclasses import dataclass
from typing import List, NamedTuple

import requests
from bs4 import BeautifulSoup

from thelatinlibrary import settings
from .section import Section
from .tome import Tome

_endpoint = "http://www.thelatinlibrary.com/"
_exceptions = ["christian.html", "classics.html", "index.html",
               "medieval.html", "misc.html", "neo.html", "readme.html"]

Works = NamedTuple('Works', [('sections', List[Section]), ('tomes', List[Tome])])


@dataclass
class Author:
    """
    The Author class represents a
    latin author/writer.
    """

    link: str
    """
    The link to the author.
    """

    name: str
    """
    The name of the author.
    """

    _works = Works([], [])
    """
    Used to store the result of the
    works getter.
    """

    @property
    def works(self) -> Works:
        """
        A list of all the books the author
        have written.

        Example:
            You can get what an author wrote using this method.

            >>> import thelatinlibrary
            >>> caesar = thelatinlibrary.get_author("http://www.thelatinlibrary.com/caes.html")
            >>> caesar
            Author(link='http://www.thelatinlibrary.com/caes.html', name='Caesar')
            >>> caesar.works
            Works(sections=[Section(name='COMMENTARIORUM LIBRI VII DE BELLO GALLICO CUM A. HIRTI SUPPLEMENTO',
            ..., tomes=[])
        """
        if settings.save and self._works.count([]) < 2:
            return self._works

        text = requests.get(self.link).text
        parser = BeautifulSoup(text, "html5lib")

        if '404' in parser.title.string:
            works = Works([], [])

            if settings.save_on_error:
                self._works = works

            return works

        sections = []
        tomes = []

        tables = list(parser.find_all("table"))
        titles = list(filter(lambda tag: 'work' not in tag.attrs, parser.find_all("div")))
        work_attributes = parser.find_all("h2", class_="work")
        works = list(filter(lambda tag: 'class' not in tag.attrs and tag.text,
                            parser.find_all("p")))

        if work_attributes:
            div_works = list(parser.find_all("div", class_="work"))

            for work_title in work_attributes:
                work_link = work_title.find("a")
                title = work_title.text.strip().rstrip()

                if work_link and work_link.text.strip().rstrip() == title:
                    tomes.append(Tome(link=_endpoint + work_link['href'],
                                      name=title.strip().rstrip()))
                elif ":" in title:
                    title_links = list(work_title.find_all("a"))

                    if title_links:
                        section = Section(tomes=[], name=title[:title.index(":")].strip().rstrip())

                        for title_link in title_links:
                            if 'href' not in title_link.attrs:
                                continue

                            section.tomes.append(Tome(link=_endpoint + title_link['href'],
                                                      name=title_link.string.strip().rstrip()))

                        sections.append(section)
                else:
                    sections.append(Section(tomes=[], name=" ".join(work_title.strings)))

            for index, section in enumerate(sections):
                try:
                    links = div_works[index].find_all("a")

                    for link in links:
                        if 'href' not in link.attrs:
                            continue

                        section.tomes.append(Tome(link=_endpoint + link['href'], name=link.string.strip().rstrip()))

                    div_works.pop(index)
                except IndexError:
                    continue

            if div_works:
                for div_work in div_works:
                    links = div_work.find_all("a")

                    for link in links:
                        if 'href' not in link.attrs:
                            continue

                        sections[-1].tomes.append(Tome(link=_endpoint + link['href'],
                                                       name=link.string.strip().rstrip()))
        else:
            tables = tables[:-1]

            if len(titles) == len(tables):
                try:
                    for div, table in zip(titles, tables):
                        if not div.text:
                            continue

                        section = Section(tomes=[], name=div.text.strip().rstrip())
                        links = table.find_all("a")

                        for work_link in links:
                            if 'href' not in work_link.attrs:
                                continue

                            section.tomes.append(Tome(link=_endpoint + work_link['href'],
                                                      name=work_link.string.strip().rstrip()))

                        sections.append(section)
                except ValueError:
                    pass
            elif len(tables) in [2, 3] and len(works) in [1, 2]:
                title_table, books_table = tables[0], tables[1]
                title = title_table.text and title_table.text.strip().rstrip()

                if title:
                    section = Section(tomes=[], name=title)
                    links = books_table.find_all("a")

                    for work_link in links:
                        if 'href' not in work_link.attrs:
                            continue

                        section.tomes.append(Tome(link=_endpoint + work_link['href'],
                                                  name=work_link.string.strip().rstrip()))

                    sections.append(section)
            else:
                for index, title in enumerate(titles):
                    link = title.find("a")

                    if link:
                        if 'href' not in link.attrs or not link.string:
                            continue

                        tomes.append(Tome(link=_endpoint + link['href'], name=link.string.strip().rstrip()))
                    else:
                        if not title.string:
                            continue

                        links = works[index].find_all("a")
                        section = Section(tomes=[], name=title.string.strip().rstrip())

                        for book_link in links:
                            if 'href' not in book_link.attrs:
                                continue

                            section.tomes.append(Tome(link=_endpoint + book_link['href'],
                                                      name=book_link.string.strip().rstrip()))

                        sections.append(section)

        for work in works:
            tables = list(work.find_all("table"))

            if len(tables) > 1:
                title_table = tables[0].find_all("td")

                if title_table and len(title_table) == 1:
                    links = work.find_all("a")
                    section = Section(tomes=[], name=tables[0].find("td").text.strip().rstrip())

                    for link in links:
                        if 'href' not in link.attrs:
                            continue

                        if link['href'] in _exceptions:
                            continue

                        if link.text and link.text.strip().rstrip() != section.name:
                            section.tomes.append(Tome(link=_endpoint + link['href'], name=link.text.strip().rstrip()))

                    sections.append(section)

        if not tomes:
            links = parser.find_all("a")

            for link in links:
                if 'href' not in link.attrs:
                    continue

                if link['href'] in _exceptions or any(map(lambda s: s.contains(_endpoint + link['href']), sections)):
                    continue

                if link.string:
                    tomes.append(Tome(link=_endpoint + link['href'], name=link.string.strip().rstrip()))

                font = link.find("font")

                if font:
                    tomes.append(Tome(link=_endpoint + link['href'], name=font.text.strip().rstrip()))

        if not tomes and not sections:
            tomes.append(Tome(link=self.link, name=self.name))

        works = Works(sections, tomes)

        if settings.save:
            self._works = works

        return works
