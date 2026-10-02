"""Bookmark mixin — infrastructure for cross-references."""
from typing import Optional

from ..styles import BOOKMARK_PREFIX


class BookmarkMixin:
    """Provides unique bookmark ids and name preparation.

    Used by TableMixin and ImageMixin to create anchors for captions,
    which are then referenced from text via the `ref()` inline node.
    """

    _bookmark_counter: int

    def __init__(self) -> None:
        super().__init__()
        self._bookmark_counter = 0

    def next_bookmark_id(self) -> int:
        """Return a fresh document-unique bookmark id."""
        self._bookmark_counter += 1
        return self._bookmark_counter

    def _prepare_bookmark(
        self,
        name: Optional[str],
        kind: str = 'element',
    ) -> tuple[Optional[str], Optional[int]]:
        """Return (full_name, id) for a user-facing bookmark name.

        Args:
            name: user-facing name, or None for no bookmark.
            kind: label used in error messages ('table', 'image', ...).

        Returns:
            A (full_name, id) tuple, or (None, None) when name is None.
        """
        if name is None:
            return None, None
        if not name.strip():
            raise ValueError(f'{kind} name must be a non-empty string')
        if any(c.isspace() for c in name):
            raise ValueError(
                f'{kind} name must not contain whitespace: {name!r}'
            )
        return f'{BOOKMARK_PREFIX}{name}', self.next_bookmark_id()