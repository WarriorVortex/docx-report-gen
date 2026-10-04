"""Imperative free-function API over a single lazy Report.

Import and call functions directly. The underlying Report is created
on the first block-level call; importing the module creates nothing.

Example:

    from docx_report_gen.writer import *

    title('Отчёт')
    h1('Введение')
    p('Формула: ', f('E = mc^2'))
    code.block('def f(x):\\n    return x ** 2')
    save('out.docx')

Starting from an existing .docx:

    new(source='Титульный лист.docx')
    h1('Введение')
    p('Содержимое начинается со второй страницы.')
    save('report.docx')

Or replace the document mid-session:

    set_source('другой.docx')
    set_document(opened_docx)

Accessor pattern:

    f('latex')            -> returns an Inline Formula node
    f.block('latex')      -> adds a block formula paragraph

    code('text')          -> returns an Inline CodeInline node
    code.block('text')    -> adds a block code paragraph
"""
from typing import Any

from ..inline.nodes import (
    b, i, u, s, sup, sub, color, highlight, link, ref,
)
from ._blocks import (
    title,
    h1, h2, h3, h4, h5, h6,
    page_break, hr,
    p, quote, ul, ol, table, img,
    toc, update_toc, header, footer, page_numbers,
    merge_cells, merge_row, merge_col,
    save,
)
from ._code import code
from ._config import (
    apply_metadata, apply_styles, config, metadata,
    set_config, set_metadata, style,
)
from ._formula import f
from ._plugins import (
    block, inline_node, plugins,
    register_plugin, unregister_plugin, use_plugin,
)
from ._state import (
    attach, close, current, detach, has_session, new, reset,
    set_document, set_source,
)


__all__ = [
    # session management
    'new', 'reset', 'attach', 'detach', 'current', 'has_session',
    # document replacement
    'set_source', 'set_document',
    # config / metadata
    'config', 'set_config', 'apply_styles',
    'metadata', 'set_metadata', 'apply_metadata',
    'style',
    # plugins
    'register_plugin', 'unregister_plugin',
    'plugins', 'use_plugin', 'block', 'inline_node',
    # document structure
    'title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'page_break', 'hr',
    # content — block-only
    'p', 'quote', 'ul', 'ol', 'table', 'img',
    'merge_cells', 'merge_row', 'merge_col',
    # page furniture
    'toc', 'update_toc', 'header', 'footer', 'page_numbers',
    # lifecycle
    'save', 'close',
    # accessors
    'f', 'code',
    # inline factories
    'b', 'i', 'u', 's', 'sup', 'sub', 'color', 'highlight',
    'link', 'ref',
]


def __getattr__(name: str) -> Any:
    """Delegate unknown attributes to the current Report."""
    if name.startswith('_'):
        raise AttributeError(name)
    report = current()
    try:
        return getattr(report, name)
    except AttributeError:
        raise AttributeError(
            f"writer has no attribute {name!r}; "
            f"no such method on Report or its plugins"
        ) from None