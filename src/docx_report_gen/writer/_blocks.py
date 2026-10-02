"""Block-level delegations to Report.

`f` (formula) and `code` (code) are defined in _formula.py and
_code.py — they do not delegate directly, because a bare call returns
an Inline node rather than adding content. Use `f.block(...)` and
`code.block(...)` for block-level forms.
"""
from typing import Any, Callable

from ._state import current


def _block(name: str) -> Callable[..., None]:
    """Return a free function delegating to Report.<name>.

    The returned function is imperative: it returns None. Chains are
    intentionally not supported here — use the Report object directly
    when chaining is needed.
    """
    def method(*args: Any, **kwargs: Any) -> None:
        getattr(current(), name)(*args, **kwargs)
    method.__name__ = name
    method.__qualname__ = f'writer.{name}'
    method.__doc__ = f'Delegate to Report.{name}().'
    return method


# document structure
title = _block('title')
h1 = _block('h1')
h2 = _block('h2')
h3 = _block('h3')
h4 = _block('h4')
h5 = _block('h5')
h6 = _block('h6')
page_break = _block('page_break')
hr = _block('hr')

# content (block-only)
p = _block('p')
quote = _block('quote')
ul = _block('ul')
ol = _block('ol')
table = _block('table')
img = _block('img')

# page furniture
toc = _block('toc')
update_toc = _block('update_toc')
header = _block('header')
footer = _block('footer')
page_numbers = _block('page_numbers')

# table merges — bound to the most recently created table
merge_cells = _block('merge_cells')
merge_row = _block('merge_row')
merge_col = _block('merge_col')


def save(path: str) -> None:
    """Write the current Report to path. Terminal operation.

    Does not reset the session — continue writing after save and call
    save() again to a different path if needed.
    """
    current().save(path)