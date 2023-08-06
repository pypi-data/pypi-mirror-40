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
from typing import List, Tuple

import requests
from bs4 import BeautifulSoup

from .section import Section
from .tome import Tome

_endpoint = "http://www.thelatinlibrary.com/"
_exceptions = ["classics.html", "index.html", "readme.html"]


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

    @property
    def works(self) -> Tuple[List[Section], List[Tome]]:
        """
        A list of all the books the author
        have written.
        """
        text = requests.get(self.link).text
        parser = BeautifulSoup(text, "html.parser")

        if '404' in parser.title.string:
            return [], []

        sections = []
        tomes = []

        work_attributes = parser.find_all("h2", class_="work")
        works = list(parser.find_all("p"))

        if work_attributes:
            div_works = list(parser.find_all("div", class_="work"))

            for work_title in work_attributes:
                sections.append(Section(tomes=[], name=" ".join(work_title.strings)))

            for index, section in enumerate(sections):
                try:
                    links = div_works[index].find_all("a")

                    for link in links:
                        section.tomes.append(Tome(link=_endpoint + link['href'], name=link.string))
                except IndexError:
                    continue
        else:
            titles = parser.find_all("div")

            for index, title in enumerate(titles):
                link = title.find("a")

                if link:
                    tomes.append(Tome(link=_endpoint + link['href'], name=link.string))
                else:
                    links = works[index].find_all("a")
                    section = Section(tomes=[], name=title.string)

                    for book_link in links:
                        section.tomes.append(Tome(link=book_link['href'], name=book_link.string))

                    sections.append(section)

        if not tomes:
            links = parser.find_all("a")

            for link in links:
                font = link.find("font")

                if font:
                    tomes.append(Tome(link=_endpoint + link['href'], name=font.string))

            if not tomes:
                tomes.append(Tome(link=self.link, name=self.name))

        return sections, tomes
