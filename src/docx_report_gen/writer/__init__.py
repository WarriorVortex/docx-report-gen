"""Imperative free-function API over a single lazy Report.

Import and call functions directly. The underlying Report is created
on the first block-level call; importing the module creates nothing.

Example:

    from docx_report_gen.writer import *

    title('Отчёт')
    h1('Введение')
    p('Формула: ', f('E = mc^2'))
    table([['A', 'B'], [1, 2]], caption='Данные')
    save('out.docx')

Runtime configuration:

    set_config(StylesConfig(font='Arial'))   # replaces and re-applies
    set_metadata(DocumentMetadata(author='X'))
    apply_styles()                            # after in-place config edit
    sync_metadata()                           # flush metadata to core props

The public surface is assembled from four submodules:

    _state     session lifecycle: new, attach, detach, current, ...
    _config    config, metadata and style accessors
    _plugins   plugin registration and local block/inline shortcuts
    _blocks    block-level delegations (h1..h6, p, table, ...)

Block-level functions return None. For chained calls, use the Report
object API directly.
"""
from typing import Any

# Inline factories are imported from the source module (nodes.py)
# rather than the inline package's __init__. Some IDEs resolve
# re-export chains poorly when a package also defines a module-level
# __getattr__ (which this file does). Importing from .nodes gives
# the IDE a concrete module with concrete `def` statements to bind.
from ..inline.nodes import (
    b, i, u, s, sup, sub, color, highlight, f, link, ref,
)
from ._blocks import (
    title,
    h1, h2, h3, h4, h5, h6,
    page_break, hr,
    p, quote, ul, ol, code, table, img,
    toc, update_toc, header, footer, page_numbers,
    merge_cells, merge_row, merge_col,
    formula, save,
)
from ._config import (
    apply_styles, config, metadata, set_config, set_metadata,
    style, sync_metadata,
)
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
    # content
    'p', 'formula', 'quote', 'ul', 'ol', 'code', 'table', 'img',
    'merge_cells', 'merge_row', 'merge_col',
    # page furniture
    'toc', 'update_toc', 'header', 'footer', 'page_numbers',
    # lifecycle
    'save', 'close',
    # inline factories
    'b', 'i', 'u', 's', 'sup', 'sub', 'color', 'highlight',
    'f', 'link', 'ref',
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