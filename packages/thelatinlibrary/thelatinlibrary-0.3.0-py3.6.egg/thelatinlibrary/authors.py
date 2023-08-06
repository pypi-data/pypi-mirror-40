# This file is a part of thelatinlibrary
#
# Copyright (c) 2019 The thelatinlibrary Authors (see AUTHORS)
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
from typing import List, NamedTuple, Optional

import requests
from bs4 import BeautifulSoup

from thelatinlibrary import settings
from thelatinlibrary.section import Section
from thelatinlibrary.tome import Tome
from thelatinlibrary.tools import titleize

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

    def works(self, reload: Optional[bool] = None, save: Optional[bool] = None,
              save_on_error: Optional[bool] = None) -> Works:
        """
        A list of all the books the author
        have written.

        Args:
            reload (Optional[bool]): If the response should be reloaded and the already stored content ignored.
            save (Optional[bool]): If the response should be saved.
            save_on_error (Optional[bool]): If the response should be saved even if an error is encountered.

        Example:
            You can get what an author wrote using this method.

            >>> import thelatinlibrary
            >>> caesar = thelatinlibrary.get_author("http://www.thelatinlibrary.com/caes.html")
            >>> caesar
            Author(link='http://www.thelatinlibrary.com/caes.html', name='Caesar')
            >>> caesar.works()
            Works(sections=[Section(name='Commentariorum Libri VII De Bello Gallico Cum A. Hirti Supplemento',
            ..., tomes=[])

        Returns:
            Works: All the works from the author.
        """
        if reload is None:
            reload = settings.reload

        if save is None:
            save = settings.save

        if save_on_error is None:
            save_on_error = settings.save_on_error

        if not reload and self._works.count([]) < 2:
            return self._works

        text = requests.get(self.link).text
        parser = BeautifulSoup(text, "html5lib")

        if '404' in parser.title.string:
            works = Works([], [])

            if save_on_error:
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
                                      name=titleize(title)))
                elif ":" in title:
                    title_links = list(work_title.find_all("a"))

                    if title_links:
                        section = Section(tomes=[], name=titleize(title[:title.index(":")]))

                        for title_link in title_links:
                            if 'href' not in title_link.attrs:
                                continue

                            section.tomes.append(Tome(link=_endpoint + title_link['href'],
                                                      name=titleize(title_link.string)))

                        sections.append(section)
                else:
                    sections.append(Section(tomes=[], name=titleize(" ".join(work_title.strings))))

            for index, section in enumerate(sections):
                try:
                    links = div_works[index].find_all("a")

                    for link in links:
                        if 'href' not in link.attrs:
                            continue

                        section.tomes.append(Tome(link=_endpoint + link['href'], name=titleize(link.string)))

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
                                                       name=titleize(link.string)))
        else:
            tables = tables[:-1]

            if len(titles) == len(tables):
                try:
                    for div, table in zip(titles, tables):
                        if not div.text:
                            continue

                        section = Section(tomes=[], name=titleize(div.text.strip))
                        links = table.find_all("a")

                        for work_link in links:
                            if 'href' not in work_link.attrs:
                                continue

                            section.tomes.append(Tome(link=_endpoint + work_link['href'],
                                                      name=titleize(work_link.string)))

                        sections.append(section)
                except ValueError:
                    pass
            elif len(tables) in [2, 3] and len(works) in [1, 2]:
                title_table, books_table = tables[0], tables[1]
                title = title_table.text and title_table.text

                if title:
                    section = Section(tomes=[], name=titleize(title))
                    links = books_table.find_all("a")

                    for work_link in links:
                        if 'href' not in work_link.attrs:
                            continue

                        section.tomes.append(Tome(link=_endpoint + work_link['href'],
                                                  name=titleize(work_link.string)))

                    sections.append(section)
            else:
                for index, title in enumerate(titles):
                    link = title.find("a")

                    if link:
                        if 'href' not in link.attrs or not link.string:
                            continue

                        tomes.append(Tome(link=_endpoint + link['href'], name=titleize(link.string)))
                    else:
                        if not title.string:
                            continue

                        links = works[index].find_all("a")
                        section = Section(tomes=[], name=titleize(title.string))

                        for book_link in links:
                            if 'href' not in book_link.attrs:
                                continue

                            section.tomes.append(Tome(link=_endpoint + book_link['href'],
                                                      name=titleize(book_link.string)))

                        sections.append(section)

        for work in works:
            tables = list(work.find_all("table"))

            if len(tables) > 1:
                title_table = tables[0].find_all("td")

                if title_table and len(title_table) == 1:
                    links = work.find_all("a")
                    section = Section(tomes=[], name=titleize(tables[0].find("td").text))

                    for link in links:
                        if 'href' not in link.attrs:
                            continue

                        if link['href'] in _exceptions:
                            continue

                        if link.text and link.text.strip().rstrip() != section.name:
                            section.tomes.append(Tome(link=_endpoint + link['href'], name=titleize(link.text)))

                    sections.append(section)

        if not tomes:
            links = parser.find_all("a")

            for link in links:
                if 'href' not in link.attrs:
                    continue

                if link['href'] in _exceptions or any(map(lambda s: s.contains(_endpoint + link['href']), sections)):
                    continue

                if link.string:
                    tomes.append(Tome(link=_endpoint + link['href'], name=titleize(link.string)))

                font = link.find("font")

                if font:
                    tomes.append(Tome(link=_endpoint + link['href'], name=titleize(font.text)))

        if not tomes and not sections:
            tomes.append(Tome(link=self.link, name=titleize(self.name)))

        works = Works(sections, tomes)

        if save:
            self._works = works

        return works
