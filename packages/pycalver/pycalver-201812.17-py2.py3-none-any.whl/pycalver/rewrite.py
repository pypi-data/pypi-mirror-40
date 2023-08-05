# -*- coding: utf-8 -*-
# This file is part of the pycalver project
# https://github.com/mbarkhau/pycalver
#
# (C) 2018 Manuel Barkhau (@mbarkhau)
# SPDX-License-Identifier: MIT
"""Rewrite files, updating occurences of version strings."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import io
import difflib
import logging
import typing as typ
from . import parse
from . import config
from . import version
str = getattr(__builtins__, 'unicode', str)
log = logging.getLogger('pycalver.rewrite')


def detect_line_sep(content):
    """Parse line separator from content.

    >>> detect_line_sep('\\r\\n')
    '\\r\\n'
    >>> detect_line_sep('\\r')
    '\\r'
    >>> detect_line_sep('\\n')
    '\\n'
    >>> detect_line_sep('')
    '\\n'
    """
    if '\r\n' in content:
        return '\r\n'
    elif '\r' in content:
        return '\r'
    else:
        return '\n'


def rewrite_lines(patterns, new_version, old_lines):
    """Replace occurances of patterns in old_lines with new_version.

    >>> old_lines = ['__version__ = "v201809.0002-beta"']
    >>> patterns = ['__version__ = "{version}"']
    >>> new_lines = rewrite_lines(patterns, "v201811.0123-beta", old_lines)
    >>> assert new_lines == ['__version__ = "v201811.0123-beta"']
    """
    new_version_nfo = version.parse_version_info(new_version)
    new_version_fmt_kwargs = new_version_nfo._asdict()
    new_lines = old_lines[:]
    for m in parse.iter_matches(old_lines, patterns):
        replacement = m.pattern.format(**new_version_fmt_kwargs)
        span_l, span_r = m.span
        new_line = m.line[:span_l] + replacement + m.line[span_r:]
        new_lines[m.lineno] = new_line
    return new_lines


RewrittenFileData = typ.NamedTuple('RewrittenFileData', [('path', str), (
    'line_sep', str), ('old_lines', typ.List[str]), ('new_lines', typ.List[
    str])])


def rfd_from_content(patterns, new_version, content):
    """Rewrite pattern occurrences with version string.

    >>> patterns = ['__version__ = "{version}"']
    >>> content = '__version__ = "v201809.0001-alpha"'
    >>> rfd = rfd_from_content(patterns, "v201809.0123", content)
    >>> assert rfd.new_lines == ['__version__ = "v201809.0123"']
    """
    line_sep = detect_line_sep(content)
    old_lines = content.split(line_sep)
    new_lines = rewrite_lines(patterns, new_version, old_lines)
    return RewrittenFileData('<path>', line_sep, old_lines, new_lines)


def iter_rewritten(file_patterns, new_version):
    """Iterate over files with version string replaced.

    >>> file_patterns = {"src/pycalver/__init__.py": ['__version__ = "{version}"']}
    >>> rewritten_datas = iter_rewritten(file_patterns, "v201809.0123")
    >>> rfd = list(rewritten_datas)[0]
    >>> assert rfd.new_lines == [
    ...     '# This file is part of the pycalver project',
    ...     '# https://gitlab.com/mbarkhau/pycalver',
    ...     '#',
    ...     '# Copyright (c) 2018 Manuel Barkhau (mbarkhau@gmail.com) - MIT License',
    ...     '# SPDX-License-Identifier: MIT',
    ...     '""\"PyCalVer: Automatic CalVer Versioning for Python Packages.""\"',
    ...     '',
    ...     '__version__ = "v201809.0123"',
    ...     '',
    ... ]
    >>>
    """
    for filepath, patterns in file_patterns.items():
        with io.open(filepath, mode='rt', encoding='utf-8') as fh:
            content = fh.read()
        rfd = rfd_from_content(patterns, new_version, content)
        yield rfd._replace(path=filepath)


def diff_lines(rfd):
    """Generate unified diff.

    >>> rfd = RewrittenFileData(
    ...    path      = "<path>",
    ...    line_sep  = "\\n",
    ...    old_lines = ["foo"],
    ...    new_lines = ["bar"],
    ... )
    >>> diff_lines(rfd)
    ['--- <path>', '+++ <path>', '@@ -1 +1 @@', '-foo', '+bar']
    """
    lines = difflib.unified_diff(a=rfd.old_lines, b=rfd.new_lines, lineterm
        ='', fromfile=rfd.path, tofile=rfd.path)
    return list(lines)


def diff(new_version, file_patterns):
    """Generate diffs of rewritten files.

    >>> file_patterns = {"src/pycalver/__init__.py": ['__version__ = "{version}"']}
    >>> diff_str = diff("v201809.0123", file_patterns)
    >>> lines = diff_str.split("\\n")
    >>> lines[:2]
    ['--- src/pycalver/__init__.py', '+++ src/pycalver/__init__.py']
    >>> assert lines[6].startswith('-__version__ = "v2')
    >>> assert not lines[6].startswith('-__version__ = "v201809.0123"')
    >>> lines[7]
    '+__version__ = "v201809.0123"'
    """
    full_diff = ''
    file_path = None
    for file_path, patterns in sorted(file_patterns.items()):
        with io.open(file_path, mode='rt', encoding='utf-8') as fh:
            content = fh.read()
        rfd = rfd_from_content(patterns, new_version, content)
        rfd = rfd._replace(path=file_path)
        full_diff += '\n'.join(diff_lines(rfd)) + '\n'
    full_diff = full_diff.rstrip('\n')
    return full_diff


def rewrite(new_version, file_patterns):
    """Rewrite project files, updating each with the new version."""
    for file_data in iter_rewritten(file_patterns, new_version):
        new_content = file_data.line_sep.join(file_data.new_lines)
        with io.open(file_data.path, mode='wt', encoding='utf-8') as fh:
            fh.write(new_content)
