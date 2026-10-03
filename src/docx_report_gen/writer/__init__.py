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

Plugins in writer mode:

    Use use_plugin(name) to obtain a registered plugin for the
    current session, then call its methods directly. Plugin methods
    see `self.report`, so nothing needs to be passed explicitly:

        class MyPlugin(Plugin):
            name = 'my-plugin'
            def centered(self, text):
                self.report.p(text, align='center')

        writer.plugins().register(MyPlugin())
        writer.use_plugin('my-plugin').centered('Hello')

    Use use_plugin(MyPlugin) to look up by class, or
    use_plugin(instance) to look up by the instance's name.

Accessor pattern:

    f('latex')            -> returns an Inline Formula node
    f.block('latex')      -> adds a block formula paragraph

    code('text')          -> returns an Inline CodeInline node
    code.block('text')    -> adds a block code paragraph

Bare calls do not modify the document; the .block() methods do.

Block-level functions return None. For chained calls, use the Report
object API directly.
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
)


__all__ = [
    # session management
    'new', 'reset', 'attach', 'detach',
    'current', 'has_session',
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
    # accessors — bare call returns Inline; .block(...) adds paragraph
    'f',
    'code',
    # inline factories
    'b', 'i', 'u', 's', 'sup', 'sub', 'color', 'highlight',
    'link', 'ref',
]


def __getattr__(name: str) -> Any:
    """Delegate unknown attributes to the current Report.

    Fires only when a name is not found at module level. Enables
    access to plugin-registered block methods and inline factories
    through the writer namespace:

        import docx_report_gen.writer as writer
        writer.centered('X')       # plugin block method
        writer.boxed('text')       # plugin inline factory

    For plugins whose methods use `self.report` (not block
    registration), use `use_plugin(name)` to obtain a handle:

        writer.use_plugin('my-plugin').centered('X')
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