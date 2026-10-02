"""Mixin wiring the plugin system into a Report instance."""
import copy
from typing import TYPE_CHECKING, Any, Optional

from ..plugins import PluginsRegistry
from ..plugins import plugins as _global_plugins

if TYPE_CHECKING:
    from ..plugins import Plugin


class PluginMixin:
    """Adds a plugin registry, lifecycle hooks and attribute delegation.

    Attribute lookup order for `r.some_name`:

    1. Normal attribute lookup (methods of Report and its mixins).
    2. Block handlers in `r.plugins` (local, then parent).
    3. Inline factories in `r.plugins` (local, then parent).
    4. AttributeError.
    """

    plugins: PluginsRegistry
    _closed: bool

    def __init__(self) -> None:
        super().__init__()
        self._closed = False

    def _init_plugins(
        self,
        extra_plugins: Optional[list['Plugin']] = None,
    ) -> None:
        """Create the local registry and attach plugins.

        Called from Report.__init__ after apply() and apply_metadata().
        Sets self.plugins, which __getattr__ reads via __dict__.
        """
        self.plugins = PluginsRegistry(parent=_global_plugins, owner=self)

        for template in _global_plugins:
            clone = copy.copy(template)
            self.plugins.register(clone)

        for plugin in (extra_plugins or []):
            self.plugins.register(plugin)

    def _plugins_before_save(self, path: str) -> None:
        for plugin in self.plugins:
            plugin.before_save(self, path)

    def _plugins_after_save(self, path: str) -> None:
        for plugin in reversed(list(self.plugins)):
            plugin.after_save(self, path)

    def close(self) -> None:
        """Detach plugins and run close hooks. Idempotent."""
        if self._closed:
            return
        self._closed = True
        for plugin in self.plugins:
            plugin.before_close(self)
        for plugin in reversed(list(self.plugins)):
            plugin.after_close(self)
        self.plugins.clear()

    def __getattr__(self, name: str) -> Any:
        if name.startswith('_'):
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute {name!r}"
            )
        registry = self.__dict__.get('plugins')
        if registry is None:
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute {name!r}"
            )

        handler = registry.resolve_block(name)
        if handler is not None:
            return lambda *args, **kwargs: handler(
                self, *args, **kwargs
            )

        factory = registry.resolve_inline(name)
        if factory is not None:
            return factory

        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute {name!r}"
        )

    def __dir__(self) -> list[str]:
        base = list(super().__dir__())
        registry = self.__dict__.get('plugins')
        if registry is not None:
            base.extend(registry.block_names())
            base.extend(registry.inline_names())
        return sorted(set(base))