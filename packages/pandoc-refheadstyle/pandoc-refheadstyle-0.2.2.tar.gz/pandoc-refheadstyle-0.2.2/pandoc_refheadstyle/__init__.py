#!/usr/local/bin/python
# encoding=utf-8
# pylint: disable=C0103
#
# Copyright 2018, 2019 Odin Kroeger
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.
"""Pandoc filter that sets a custom style for the reference section header."""

from panflute import Div, Header, Para, stringify

DEFAULT_STYLE = 'Bibliography Heading'


class RefHeadStyleSetter():  # pylint: disable=R0903, R1710, W0201
    """Sets a custom style for the reference section header."""

    style = DEFAULT_STYLE

    def __call__(self, elem, doc):
        r"""Set a custom style for the reference section header.

        :param panflute.Element elem: A Pandoc AST element.
        :param panflute.Doc doc: The Pandoc document that is parsed.
        :returns: A ``Div`` with the custom style set to the value of\
            ``reference-header-style`` or to 'Bibliography Heading'.\
            If *elem* isn't the reference section header, returns `None`.
        :rtype: panflute.Element or None

        If -- and only if -- the metadata field ``reference-section-title`` is
        set, sets the style of the reference section header to the value of
        the metadata field ``reference-header-style`` or to 'Bibliography
        Heading' if that metadata field has not been set or is empty.

        See :func:`set_style` on how it is determined whether a header is the
        reference section header.
        """
        try:
            if self.title:
                return set_style(elem, self.title, self.style)
        except AttributeError:
            self.title = doc.get_metadata('reference-section-title')
            style = doc.get_metadata('reference-header-style')
            if style:
                self.style = style
        return self(elem, doc)


def set_style(elem, title, style):  # pylint: disable=R1710
    r"""Change the style of the reference heading.

    :param panflute.Element elem: A Pandoc AST element.
    :param panflute.Doc doc: The Pandoc document that is parsed.
    :param str title: The title of the reference section.
    :param str style: The style of the reference section header.
    :returns: A ``Div`` with the custom style set to the value of\
        ``reference-header-style`` or to 'Bibliography Heading'.
        If *elem* isn't the reference section header, returns ``None``.
    :rtype: panflute.Element or None

    *elem* is considered the reference section header if and only if:
        1. It is an instance of Header.
        2. Its ID is 'bibliography'.
        3. Its text is the value of *title*.
    """
    if (isinstance(elem, Header) and
            elem.identifier == 'bibliography' and
            stringify(elem) == title):
        attributes = elem.attributes
        attributes['custom-style'] = style
        return Div(Para(*elem.content), identifier=elem.identifier,
                   classes=elem.classes, attributes=attributes)
