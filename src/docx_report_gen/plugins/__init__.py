"""Plugin system.

Usage:

    from docx_report_gen.plugins import plugins, Plugin

    class MyPlugin(Plugin):
        name = 'my-plugin'

        def setup(self, report):
            report.page_numbers()

    plugins.register(MyPlugin())

The global `plugins` registry holds templates applied to every Report
created after registration. Each Report also exposes its own registry
at `report.plugins`, sharing the same API.
"""
from .base import Plugin
from .registry import PluginsRegistry


# Global registry. Plugins registered here are templates cloned into
# each new Report. Inline and block registrations made directly on
# this object are visible to every Report through the parent chain.
plugins = PluginsRegistry()


__all__ = ['Plugin', 'PluginsRegistry', 'plugins']