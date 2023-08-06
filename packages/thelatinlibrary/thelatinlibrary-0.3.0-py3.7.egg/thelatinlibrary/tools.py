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

import re
from html import unescape

roman_numerals = re.compile(r"\b(?=[MDCLXVI]+\b)M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\b", re.IGNORECASE)


def titleize(title: str):
    """
    Format a title including roman numerals.

    Args:
      title (str): The string you want to format.

    Example:
        >>> from thelatinlibrary.tools import titleize
        >>> titleize("de bello gallico")
        'De Bello Gallico'
        >>> titleize("liber i")
        'Liber I'
        >>> titleize("liber ii")
        'Liber II'
        >>> titleize("liber lvxig")
        'Liber Lvxig'

    Returns:
      str: The formatted title.
    """
    return roman_numerals.sub(lambda number: number.group().upper(), unescape(title.title().strip().rstrip()))
