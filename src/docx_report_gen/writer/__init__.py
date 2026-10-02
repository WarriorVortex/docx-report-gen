"""Imperative free-function API over a single lazy Report.

Import and call functions directly. The underlying Report is created
on the first block-level call; importing the module creates nothing.

Example:

    from docx_report_gen.writer import *

    title('Отчёт')
    h1('Введение')
    p('Формула: ', f('E = mc^2'))            # inline formula
    p('Функция ', code('print'), ' выводит') # inline code
    f.block('E = mc^2')                       # block formula
    code.block('def f(x):\\n    return x ** 2')  # block code
    table([['A', 'B'], [1, 2]], caption='Данные')
    save('out.docx')

Accessor pattern:

    f('latex')            -> returns an Inline Formula node
    f.block('latex')      -> adds a block formula paragraph

    code('text')          -> returns an Inline CodeInline node
    code.block('text')    -> adds a block code paragraph

Bare calls do not modify the document; the .block() methods do.

Runtime configuration:

    set_config(StylesConfig(font='Arial'))
    set_metadata(DocumentMetadata(author='X'))
    apply_styles()
    sync_metadata()

Block-level functions return None. For chained calls, use the Report
object API directly.
"""
from typing import Any

# Inline factories are imported from the source module (nodes.py)
# rather than the inline package's __init__. Some IDEs resolve
# re-export chains poorly when a package also defines a module-level
# __getattr__ (which this file does). Importing from .nodes gives
# the IDE a concrete module with concrete `def` statements to bind.
# `f` and `code` are imported from their accessor modules instead.
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
    apply_styles, config, metadata, set_config, set_metadata,
    style, sync_metadata,
)
from ._formula import f
from ._plugins import (
    block, inline_node, plugins,
    register_plugin, unregister_plugin,
)
from ._state import (
    attach, close, configure, current, detach, has_session, new, reset,
)


__all__ = [
    # session management
    'new', 'configure', 'reset', 'attach', 'detach',
    'current', 'has_session',
    # config / metadata
    'config', 'set_config', 'apply_styles',
    'metadata', 'set_metadata', 'sync_metadata',
    'style',
    # plugins
    'register_plugin', 'unregister_plugin',
    'plugins', 'block', 'inline_node',
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
    # accessors — bare call returns Inline; .block(...) adds paragraph
    'f',     # formula:  f('x^2') / f.block('x^2')
    'code',  # code:     code('print') / code.block('def f(): ...')
    # inline factories
    'b', 'i', 'u', 's', 'sup', 'sub', 'color', 'highlight',
    'link', 'ref',
]


def __getattr__(name: str) -> Any:
    """Delegate unknown attributes to the current Report.

    Fires only when a name is not found at module level. Enables
    access to plugin-registered methods and inline factories through
    the writer namespace:

        import docx_report_gen.writer as writer
        writer.centered('X')       # plugin block method
        writer.boxed('text')       # plugin inline factory
    """
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