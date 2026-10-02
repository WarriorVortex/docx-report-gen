"""Plugin base class."""
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from ..report import Report
    from .registry import PluginsRegistry


class Plugin:
    """Base class for report extensions.

    A plugin extends a Report in three ways:

    1. Registers block methods on the report:
           self.registry.block('centered', handler)

    2. Registers inline node factories:
           self.registry.inline('boxed', factory)

    3. Reacts to lifecycle events by overriding hooks:
           setup(report)
           before_save(report, path)
           after_save(report, path)
           before_close(report)
           after_close(report)

    Plugins do not need to subclass Plugin — any object exposing a
    `setup` method and a unique `name` attribute is accepted. The base
    class provides sensible defaults and auto-names unnamed subclasses
    after their class name.
    """

    name: Optional[str] = None

    def __init__(self) -> None:
        self.report: Optional['Report'] = None
        self.registry: Optional['PluginsRegistry'] = None

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if cls.__dict__.get('name') is None:
            cls.name = cls.__name__

    # ---------- lifecycle hooks ----------

    def setup(self, report: 'Report') -> None:
        """Called once when the plugin is attached to a Report."""

    def before_save(self, report: 'Report', path: str) -> None:
        """Called before the document is written to disk."""

    def after_save(self, report: 'Report', path: str) -> None:
        """Called after the document has been written to disk."""

    def before_close(self, report: 'Report') -> None:
        """Called before the plugin is detached from the Report."""

    def after_close(self, report: 'Report') -> None:
        """Called after the plugin has been detached."""