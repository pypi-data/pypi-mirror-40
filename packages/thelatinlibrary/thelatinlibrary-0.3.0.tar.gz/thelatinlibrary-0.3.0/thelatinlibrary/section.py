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

from typing import List

from dataclasses import dataclass

from thelatinlibrary.tome import Tome


@dataclass
class Section:
    """
    The Section class represents a
    selection of books written by a
    latin author.
    """

    name: str
    """
    The name of the section.
    """

    tomes: List[Tome]
    """
    The tomes contained into the section.
    """

    def contains(self, link: str) -> bool:
        """
        Used to know if a link is already contained
        into the section.

        Args:
            link (str): The link that is being checked.

        Example:
            You can check if a link is contained into this section by using
            this method.

            >>> import thelatinlibrary
            >>> caesar = thelatinlibrary.get_author("http://www.thelatinlibrary.com/caes.html")
            >>> caesar
            Author(link='http://www.thelatinlibrary.com/caes.html', name='Caesar')
            >>> caesar.works()
            Works(sections=[Section(name='Commentariorum Libri VII De Bello Gallico Cum A. Hirti Supplemento',
            ..., tomes=[])
            >>> section = caesar.works().sections[0]
            >>> section.contains("http://www.thelatinlibrary.com/caesar/gall1.shtml")
            True
            >>> section.contains("http://www.thelatinlibrary.com/caesar/bc3.shtml")
            False

        Returns:
            bool: True if the link is found, otherwise False.
        """
        return any(map(lambda tome: link == tome.link, self.tomes))
