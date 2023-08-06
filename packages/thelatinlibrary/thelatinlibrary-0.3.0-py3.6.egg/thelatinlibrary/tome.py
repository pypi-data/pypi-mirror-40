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
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

from thelatinlibrary import settings


@dataclass
class Tome:
    """
    The Tome class represents one of the
    multiple volumes used to write a book.
    """

    link: str
    """
    The link to the tome.
    """

    name: str
    """
    The name of the tome.
    """

    _text = ""
    """
    Used to store the result of the
    text getter.
    """

    def text(self, reload: Optional[bool] = None, save: Optional[bool] = None) -> List[str]:
        """
        The text contained in the tome.

        Args:
            reload (Optional[bool]): If the response should be reloaded and the already stored content ignored.
            save (Optional[bool]): If the response should be saved.

        Example:
            You can get what an author wrote in a tome using this method.

            >>> import thelatinlibrary
            >>> caesar = thelatinlibrary.get_author("http://www.thelatinlibrary.com/caes.html")
            >>> caesar
            Author(link='http://www.thelatinlibrary.com/caes.html', name='Caesar')
            >>> works = caesar.works()
            >>> works
            Works(sections=[Section(name='Commentariorum Libri VII De Bello Gallico Cum A. Hirti Supplemento',
            ..., tomes=[])
            >>> de_bello_gallico = works.sections[0]
            >>> de_bello_gallico
            Section(name='Commentariorum Libri VII De Bello Gallico Cum A. Hirti Supplemento', ...
            Tome(link='http://www.thelatinlibrary.com/caesar/gall8.shtml', name='Liber VIII')])
            >>> tome = de_bello_gallico.tomes[0]
            >>> tome
            Tome(link='http://www.thelatinlibrary.com/caesar/gall1.shtml', name='Liber I')
            >>> tome.text()
            ['[1] 1 Gallia est omnis divisa in partes tres, ...', ..., '...ad conventus agendos profectus est.']

        Return:
            List[str]: All the paragraphs of the tome.
        """
        if reload is None:
            reload = settings.reload

        if save is None:
            save = settings.save

        if not reload and self._text:
            return self._text

        text = requests.get(self.link).text
        parser = BeautifulSoup(text, "html5lib")

        if '404' in parser.title.string:
            return []

        paragraphs = []
        texts = list(parser.find_all("p"))[1:-1]

        for text in texts:
            paragraphs.append(text.text.strip().rstrip())

        if save:
            self._text = paragraphs

        return paragraphs
