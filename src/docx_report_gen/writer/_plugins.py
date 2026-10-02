"""Plugin helpers for the writer singleton."""
from typing import Any, Callable, cast

from ..plugins import (
    Plugin,
    PluginsRegistry,
    plugins as _global_plugins,
)
from ._state import current


# Handlers and factories are user-provided callables with arbitrary
# signatures. The registry validates them at runtime; typing here
# stays loose on purpose.
BlockHandler = Callable[..., Any]
InlineFactory = Callable[..., Any]


def register_plugin(plugin: Plugin) -> Plugin:
    """Register a plugin in the global registry.

    Applies to every Report created *after* this call. The current
    session, if any, is not modified — use `plugins().register(...)`
    to attach a plugin to the current Report only.

    Returns:
        The registered plugin, for convenience.
    """
    # PluginsRegistry.register returns Any because plugins are
    # duck-typed (any object with setup + name). We know the concrete
    # type here: it is the same object that was passed in.
    return cast(Plugin, _global_plugins.register(plugin))


def unregister_plugin(plugin: Plugin) -> None:
    """Remove a plugin from the global registry.

    Reports already created are unaffected.
    """
    _global_plugins.unregister(plugin)


def plugins() -> PluginsRegistry:
    """Return the current Report's local plugin registry.

    Use it to attach a plugin to this Report only, or to register
    custom inline nodes and block methods.
    """
    return current().plugins


def block(name: str, handler: BlockHandler) -> None:
    """Register a block method on the current Report.

    Shortcut for plugins().block(name, handler). The handler is
    invoked as handler(report, *args, **kwargs).
    """
    current().plugins.block(name, handler)


def inline_node(name: str, factory: InlineFactory) -> None:
    """Register an inline node factory on the current Report.

    Shortcut for plugins().inline(name, factory). The factory is
    invoked as factory(*args, **kwargs) and must return an Inline.
    """
    current().plugins.inline(name, factory)