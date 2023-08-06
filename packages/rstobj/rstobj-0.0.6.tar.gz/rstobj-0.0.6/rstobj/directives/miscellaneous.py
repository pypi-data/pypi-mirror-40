# -*- coding: utf-8 -*-

"""
Other directives.
"""

import attr
from .base import Directive


@attr.s
class Include(Directive):
    """
    ``.. include::`` directive. Include an external document fragment.

    Example::

        inc = Include(path="README.rst")
        inc.render()

    Output::

        .. include:: README.rst

    Parameters definition see here http://docutils.sourceforge.net/docs/ref/rst/directives.html#including-an-external-document-fragment.
    """
    path = attr.ib(default=None)
    start_line = attr.ib(default=None)
    end_line = attr.ib(default=None)
    start_after = attr.ib(default=None)
    end_before = attr.ib(default=None)
    literal = attr.ib(default=None)
    code = attr.ib(default=None)
    number_lines = attr.ib(default=None)
    encoding = attr.ib(default=None)
    tab_width = attr.ib(default=None)

    meta_directive_keyword = "include"
    meta_not_none_fields = ("path",)

    @property
    def arg(self):
        return self.path
