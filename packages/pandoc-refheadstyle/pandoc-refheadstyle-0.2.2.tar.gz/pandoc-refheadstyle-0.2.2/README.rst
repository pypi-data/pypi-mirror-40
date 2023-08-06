===================
pandoc-refheadstyle
===================

``pandoc-refheadstyle`` sets a custom style for the reference section
header, that is, if the metadata field ``reference-section-title`` has been
set to a non-empty value.

By default, the reference section header will be assigned the custom style
'Bibliography Heading'. But you can assign another style by setting the
metadata field ``reference-header-style`` to the name of a style of your
choice. If the style does not exist, it will be created.

By fiat, a reference section header is any header that has the ID
'bibliography' and the header text set in ``reference-section-title``.
(A header inserted by ``pandoc-citeproc`` will meet these criteria.)

If you are using `Pandoc <https://www.pandoc.org/>`_ 2.0 or newer,
you will want to use `pandoc-refheadstyle.lua
<https://github.com/odkr/pandoc-refheadstyle.lua>`_ instead; it's
easier to install and faster.


Synopsis
========

pandoc-refheadstyle [-h]

pandoc [...] -F pandoc-refheadstyle [...]


Installing ``pandoc-refheadstyle``
==================================

You use ``pandoc-refheadstyle`` **at your own risk**. You have been warned.

You need `Python <https://www.python.org/>`_ 2.7 or newer and
`panflute <https://github.com/sergiocorreia/panflute>`_.

Simply run::

    pip install pandoc_refheadstyle


Contact
=======

If there's something wrong with ``pandoc-refheadstyle``, `open an issue
<https://github.com/odkr/pandoc-refheadstyle/issues>`_.


License
=======

Copyright 2018 Odin Kroeger

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


Further Information
===================

GitHub:
<https://github.com/odkr/pandoc-refheadstyle>

PyPI:
<https://pypi.org/project/pandoc-refheadstyle>


See also
========

`pandoc-refheadstyle.lua
<https://github.com/odkr/pandoc-refheadstyle.lua>`_
