"""Plugin helpers for the writer singleton."""
from typing import Any, Callable, Union, cast

from ..plugins import (
    Plugin,
    PluginsRegistry,
    plugins as _global_plugins,
)
from ._state import current


BlockHandler = Callable[..., Any]
InlineFactory = Callable[..., Any]

# use_plugin accepts three forms: name, class, instance.
PluginRef = Union[str, type, Plugin]


def register_plugin(plugin: Plugin) -> Plugin:
    """Register a plugin in the global registry.

    Applies to every Report created *after* this call. The current
    session, if any, is not modified — use `plugins().register(...)`
    to attach a plugin to the current Report only.

    Returns:
        The registered plugin, for convenience.
    """
    return cast(Plugin, _global_plugins.register(plugin))


def unregister_plugin(plugin: Plugin) -> None:
    """Remove a plugin from the global registry."""
    _global_plugins.unregister(plugin)


def plugins() -> PluginsRegistry:
    """Return the current Report's local plugin registry.

    Use it to attach a plugin to this Report only, or to register
    custom inline nodes and block methods.
    """
    return current().plugins


def use_plugin(plugin: PluginRef) -> Any:
    """Return a plugin handle for the current session.

    Accepts:
        use_plugin('my-plugin')    # by name
        use_plugin(MyPlugin)       # by class — uses cls.name
        use_plugin(instance)       # by instance — uses instance.name

    The returned object is the plugin clone attached to the current
    Report. Its methods see `self.report`, so they can be called
    without passing the Report explicitly:

        class MyPlugin(Plugin):
            name = 'my-plugin'
            def centered(self, text):
                self.report.p(text, align='center')

        writer.plugins().register(MyPlugin())
        writer.use_plugin('my-plugin').centered('Hello')

    Raises:
        KeyError: plugin with that name is not visible. The error
            message lists available names.
    """
    if isinstance(plugin, str):
        name = plugin
    else:
        name = getattr(plugin, 'name', None) or type(plugin).__name__
    return current().plugins.resolve(name)


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