"""Registry of plugins, block methods and inline node factories.

Two instances of this class exist in a running program:

- The global instance (``docx_report_gen.plugins.plugins``). It holds
  plugin templates and registrations that apply to every Report
  created from now on.
- A per-Report instance (``report.plugins``), created in Report.__init__
  with the global instance as parent. It holds plugin clones and
  per-instance registrations.

Lookups walk from the instance up to the parent, so local
registrations shadow global ones without raising.
"""
import copy
from typing import Any, Callable, Iterator, Optional


# Names that cannot be used for block registration: they would shadow
# real Report attributes or methods, or the mixin API.
RESERVED_BLOCKS = frozenset({
    'doc', 'config', 'metadata', 'plugins',
    'style', 'save', 'close',
    'title',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'p', 'f', 'quote',
    'ul', 'ol',
    'code',
    'table', 'merge_cells', 'merge_row', 'merge_col',
    'img',
    'toc', 'update_toc',
    'header', 'footer', 'page_numbers',
    'page_break', 'hr',
    'next_bookmark_id',
})

# Names that cannot be used for inline registration: they would shadow
# existing inline factories exported from docx_report_gen.inline.
RESERVED_INLINES = frozenset({
    'b', 'i', 'u', 's', 'sup', 'sub',
    'color', 'highlight',
    'f', 'link', 'ref',
    'Inline', 'Bold', 'Italic', 'Underline', 'Strike',
    'Sup', 'Sub', 'Color', 'Highlight', 'Formula', 'Link',
    'Reference',
})

_RESERVED = RESERVED_BLOCKS | RESERVED_INLINES

# Registry collections hold heterogeneous callables. Precise types
# would require importing from inline and mixins, creating cycles.
BlockHandler = Callable[..., Any]
InlineFactory = Callable[..., Any]


class PluginsRegistry:
    """Registry of plugins, block methods and inline node factories."""

    def __init__(self,
                 parent: Optional['PluginsRegistry'] = None,
                 owner: Any = None) -> None:
        """
        Args:
            parent: another PluginsRegistry used as fallback for
                lookups. None for the global registry.
            owner: the Report this registry belongs to. When set,
                register() attaches plugins to it and calls setup().
                None for the global registry.
        """
        self._parent = parent
        self._owner = owner
        self._plugins: dict[str, Any] = {}
        self._inline: dict[str, InlineFactory] = {}
        self._block: dict[str, BlockHandler] = {}

    # ---------- plugins ----------

    def register(self, plugin: Any) -> Any:
        """Attach a plugin to this registry.

        Validates the name, assigns `plugin.report` and
        `plugin.registry`, stores the plugin, and — when the registry
        has an owner — calls `plugin.setup(owner)`.
        """
        if not hasattr(plugin, 'setup'):
            raise TypeError(
                f'plugin must have a setup(report) method, '
                f'got {type(plugin).__name__}'
            )
        name = getattr(plugin, 'name', None)
        if not name:
            raise ValueError(
                f'plugin {type(plugin).__name__} has no name'
            )
        if name in self._plugins:
            raise ValueError(f"plugin '{name}' already registered")
        self._plugins[name] = plugin

        if hasattr(plugin, 'report'):
            plugin.report = self._owner
        if hasattr(plugin, 'registry'):
            plugin.registry = self

        if self._owner is not None:
            plugin.setup(self._owner)
        return plugin

    def unregister(self, plugin: Any) -> None:
        """Remove a plugin registered in this registry."""
        name = getattr(plugin, 'name', None)
        if name is None or name not in self._plugins:
            raise ValueError(
                f"plugin {type(plugin).__name__} is not registered"
            )
        if self._plugins[name] is not plugin:
            raise ValueError(
                f"plugin '{name}' is registered with a different instance"
            )
        del self._plugins[name]

    def get_plugin(self, name: str) -> Optional[Any]:
        """Return a plugin by name. Checks local, then parent, then None."""
        if name in self._plugins:
            return self._plugins[name]
        if self._parent is not None:
            return self._parent.get_plugin(name)
        return None

    def plugin_names(self) -> tuple[str, ...]:
        """Sorted tuple of plugin names visible from this registry."""
        names = set(self._plugins)
        if self._parent is not None:
            names |= set(self._parent.plugin_names())
        return tuple(sorted(names))

    # ---------- inline node factories ----------

    def inline(self, name: str, factory: InlineFactory) -> None:
        """Register an inline node factory under `name`."""
        if not callable(factory):
            raise TypeError(
                f'inline factory for {name!r} must be callable, '
                f'got {type(factory).__name__}'
            )
        self._register_named(
            kind='inline',
            name=name,
            value=factory,
            target=self._inline,
            other=self._block,
            other_kind='block',
        )

    def uninline(self, name: str) -> None:
        """Remove an inline factory. Silent if not present."""
        self._inline.pop(name, None)

    def resolve_inline(self, name: str) -> Optional[InlineFactory]:
        """Return the inline factory visible from this registry, or None."""
        if name in self._inline:
            return self._inline[name]
        if self._parent is not None:
            return self._parent.resolve_inline(name)
        return None

    def inline_names(self) -> frozenset[str]:
        """Frozenset of inline names visible from this registry."""
        names = set(self._inline)
        if self._parent is not None:
            names |= set(self._parent.inline_names())
        return frozenset(names)

    # ---------- block methods ----------

    def block(self, name: str, handler: BlockHandler) -> None:
        """Register a block method under `name`."""
        if not callable(handler):
            raise TypeError(
                f'block handler for {name!r} must be callable, '
                f'got {type(handler).__name__}'
            )
        self._register_named(
            kind='block',
            name=name,
            value=handler,
            target=self._block,
            other=self._inline,
            other_kind='inline',
        )

    def unblock(self, name: str) -> None:
        """Remove a block handler. Silent if not present."""
        self._block.pop(name, None)

    def resolve_block(self, name: str) -> Optional[BlockHandler]:
        """Return the block handler visible from this registry, or None."""
        if name in self._block:
            return self._block[name]
        if self._parent is not None:
            return self._parent.resolve_block(name)
        return None

    def block_names(self) -> frozenset[str]:
        """Frozenset of block names visible from this registry."""
        names = set(self._block)
        if self._parent is not None:
            names |= set(self._parent.block_names())
        return frozenset(names)

    # ---------- shared registration helper ----------

    def _register_named(
        self,
        *,
        kind: str,
        name: str,
        value: Any,
        target: dict[str, Any],
        other: dict[str, Any],
        other_kind: str,
    ) -> None:
        """Shared validation and insertion for inline and block.

        The caller is responsible for the callable() check. This method
        handles the three conflict cases:
          - reserved name (would shadow core Report API)
          - name already used by the other kind in this registry
          - name already registered under the same kind
        """
        if name in _RESERVED:
            raise ValueError(f"name '{name}' is reserved")
        if name in other:
            raise ValueError(
                f"name '{name}' is already registered as a {other_kind}"
            )
        if name in target:
            raise ValueError(f"{kind} '{name}' already registered")
        target[name] = value

    # ---------- iteration and utilities ----------

    def __iter__(self) -> Iterator[Any]:
        """Iterate over plugins registered in this registry (not parent)."""
        return iter(self._plugins.values())

    def __len__(self) -> int:
        return len(self._plugins)

    def __contains__(self, name: str) -> bool:
        return name in self._plugins

    def clone_all(self) -> Iterator[tuple[Any, Any]]:
        """Yield (clone, template) for each plugin, cloning templates."""
        for template in self._plugins.values():
            yield copy.copy(template), template

    def clear(self) -> None:
        """Remove all plugins, inline factories and block handlers."""
        self._plugins.clear()
        self._inline.clear()
        self._block.clear()