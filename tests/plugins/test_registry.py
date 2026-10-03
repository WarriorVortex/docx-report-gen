"""Tests for PluginsRegistry — registration, conflicts, parent chain."""

import pytest

from docx_report_gen.plugins import Plugin, PluginsRegistry


# ---------- test helpers ----------

class SimplePlugin:
    name = 'simple'
    def setup(self, report):
        pass


class OtherPlugin:
    name = 'other'
    def setup(self, report):
        pass


# ---------- plugin registration ----------

def test_register_plugin():
    reg = PluginsRegistry()
    plugin = SimplePlugin()
    reg.register(plugin)
    assert len(reg) == 1
    assert 'simple' in reg
    assert reg.get_plugin('simple') is plugin


def test_register_without_setup_raises():
    class Bad:
        name = 'bad'
    with pytest.raises(TypeError, match='setup'):
        PluginsRegistry().register(Bad())


def test_register_without_name_raises():
    class NoName:
        name = ''
        def setup(self, report):
            pass
    with pytest.raises(ValueError, match='name'):
        PluginsRegistry().register(NoName())


def test_duplicate_name_raises():
    reg = PluginsRegistry()
    reg.register(SimplePlugin())
    with pytest.raises(ValueError, match='already registered'):
        reg.register(SimplePlugin())


def test_register_two_plugins_with_different_names():
    reg = PluginsRegistry()
    reg.register(SimplePlugin())
    reg.register(OtherPlugin())
    assert len(reg) == 2
    assert set(reg.plugin_names()) == {'simple', 'other'}


# ---------- resolve ----------

def test_resolve_returns_registered_plugin():
    reg = PluginsRegistry()
    p = SimplePlugin()
    reg.register(p)
    assert reg.resolve('simple') is p


def test_resolve_raises_on_missing():
    reg = PluginsRegistry()
    with pytest.raises(KeyError):
        reg.resolve('missing')


def test_resolve_error_lists_available_names():
    reg = PluginsRegistry()
    reg.register(SimplePlugin())
    with pytest.raises(KeyError, match='simple'):
        reg.resolve('missing')


def test_resolve_walks_to_parent():
    parent = PluginsRegistry()
    p = SimplePlugin()
    parent.register(p)
    child = PluginsRegistry(parent=parent)
    assert child.resolve('simple') is p


def test_resolve_prefers_local_over_parent():
    parent = PluginsRegistry()
    parent.register(SimplePlugin())
    child = PluginsRegistry(parent=parent)
    local = SimplePlugin()
    child.register(local)
    assert child.resolve('simple') is local


# ---------- unregister ----------

def test_unregister_removes_plugin():
    reg = PluginsRegistry()
    plugin = SimplePlugin()
    reg.register(plugin)
    reg.unregister(plugin)
    assert len(reg) == 0
    assert reg.get_plugin('simple') is None


def test_unregister_unknown_raises():
    reg = PluginsRegistry()
    with pytest.raises(ValueError, match='not registered'):
        reg.unregister(SimplePlugin())


def test_unregister_with_different_instance_raises():
    reg = PluginsRegistry()
    a = SimplePlugin()
    b = SimplePlugin()
    reg.register(a)
    with pytest.raises(ValueError, match='different instance'):
        reg.unregister(b)


# ---------- lookup and iteration ----------

def test_get_plugin_returns_none_for_unknown():
    assert PluginsRegistry().get_plugin('nope') is None


def test_plugin_names_sorted():
    reg = PluginsRegistry()
    reg.register(OtherPlugin())
    reg.register(SimplePlugin())
    assert reg.plugin_names() == ('other', 'simple')


def test_iteration_over_plugins():
    reg = PluginsRegistry()
    p1, p2 = SimplePlugin(), OtherPlugin()
    reg.register(p1)
    reg.register(p2)
    plugins = list(reg)
    assert p1 in plugins
    assert p2 in plugins


def test_contains():
    reg = PluginsRegistry()
    reg.register(SimplePlugin())
    assert 'simple' in reg
    assert 'nope' not in reg


# ---------- inline factories ----------

def test_inline_registration():
    reg = PluginsRegistry()
    factory = lambda text: text
    reg.inline('boxed', factory)
    assert reg.resolve_inline('boxed') is factory
    assert 'boxed' in reg.inline_names()


def test_inline_non_callable_raises():
    with pytest.raises(TypeError, match='callable'):
        PluginsRegistry().inline('x', 'not callable')


def test_inline_reserved_name_raises():
    with pytest.raises(ValueError, match='reserved'):
        PluginsRegistry().inline('b', lambda: None)


def test_inline_duplicate_raises():
    reg = PluginsRegistry()
    reg.inline('custom', lambda: None)
    with pytest.raises(ValueError, match='already registered'):
        reg.inline('custom', lambda: None)


def test_inline_conflicts_with_block():
    reg = PluginsRegistry()
    reg.block('custom', lambda report: None)
    with pytest.raises(ValueError, match='block'):
        reg.inline('custom', lambda: None)


def test_uninline_removes_factory():
    reg = PluginsRegistry()
    reg.inline('x', lambda: None)
    reg.uninline('x')
    assert reg.resolve_inline('x') is None


def test_uninline_silent_on_missing():
    PluginsRegistry().uninline('never_registered')


# ---------- block handlers ----------

def test_block_registration():
    reg = PluginsRegistry()
    handler = lambda report: None
    reg.block('centered', handler)
    assert reg.resolve_block('centered') is handler
    assert 'centered' in reg.block_names()


def test_block_non_callable_raises():
    with pytest.raises(TypeError, match='callable'):
        PluginsRegistry().block('x', 'not callable')


def test_block_reserved_name_raises():
    with pytest.raises(ValueError, match='reserved'):
        PluginsRegistry().block('p', lambda report: None)


def test_block_duplicate_raises():
    reg = PluginsRegistry()
    reg.block('custom', lambda report: None)
    with pytest.raises(ValueError, match='already registered'):
        reg.block('custom', lambda report: None)


def test_block_conflicts_with_inline():
    reg = PluginsRegistry()
    reg.inline('custom', lambda: None)
    with pytest.raises(ValueError, match='inline'):
        reg.block('custom', lambda report: None)


def test_unblock_removes_handler():
    reg = PluginsRegistry()
    reg.block('x', lambda report: None)
    reg.unblock('x')
    assert reg.resolve_block('x') is None


# ---------- parent chain ----------

def test_child_sees_parent_plugin():
    parent = PluginsRegistry()
    parent.register(SimplePlugin())
    child = PluginsRegistry(parent=parent)
    assert child.get_plugin('simple') is not None
    assert 'simple' in child.plugin_names()


def test_parent_does_not_see_child_plugin():
    parent = PluginsRegistry()
    child = PluginsRegistry(parent=parent)
    child.register(SimplePlugin())
    assert parent.get_plugin('simple') is None
    assert 'simple' not in parent.plugin_names()


def test_child_lookup_walks_to_parent_for_inline():
    parent = PluginsRegistry()
    factory = lambda: None
    parent.inline('shared', factory)
    child = PluginsRegistry(parent=parent)
    assert child.resolve_inline('shared') is factory


def test_child_local_overrides_parent_inline():
    parent = PluginsRegistry()
    parent.inline('name', lambda: 'parent')
    child = PluginsRegistry(parent=parent)
    child.inline('name', lambda: 'child')
    assert child.resolve_inline('name')() == 'child'


def test_child_inline_names_include_parent():
    parent = PluginsRegistry()
    parent.inline('p_name', lambda: None)
    child = PluginsRegistry(parent=parent)
    child.inline('c_name', lambda: None)
    names = child.inline_names()
    assert 'p_name' in names
    assert 'c_name' in names


def test_child_lookup_walks_to_parent_for_block():
    parent = PluginsRegistry()
    handler = lambda report: None
    parent.block('shared', handler)
    child = PluginsRegistry(parent=parent)
    assert child.resolve_block('shared') is handler


# ---------- owner behaviour ----------

def test_register_calls_setup_when_owner_present():
    class Owner:
        pass

    owner = Owner()
    reg = PluginsRegistry(owner=owner)

    class P:
        name = 'p'
        def setup(self, report):
            self.got = report

    p = P()
    reg.register(p)
    assert p.got is owner


def test_register_sets_report_and_registry_for_plugin_subclass():
    """A full Plugin instance gets its `report` and `registry` set."""
    class Owner:
        pass

    owner = Owner()
    reg = PluginsRegistry(owner=owner)

    class P(Plugin):
        name = 'p'

    p = P()
    reg.register(p)
    assert p.report is owner
    assert p.registry is reg


def test_register_does_not_call_setup_without_owner():
    class P:
        name = 'p'
        called = False
        def setup(self, report):
            P.called = True

    reg = PluginsRegistry()   # no owner
    reg.register(P())
    assert P.called is False


# ---------- clone_all ----------

def test_clone_all_yields_copies():
    reg = PluginsRegistry()
    template = SimplePlugin()
    reg.register(template)
    pairs = list(reg.clone_all())
    assert len(pairs) == 1
    clone, returned_template = pairs[0]
    assert clone is not template
    assert returned_template is template


# ---------- clear ----------

def test_clear_removes_everything():
    reg = PluginsRegistry()
    reg.register(SimplePlugin())
    reg.inline('x', lambda: None)
    reg.block('y', lambda report: None)
    reg.clear()
    assert len(reg) == 0
    assert reg.resolve_inline('x') is None
    assert reg.resolve_block('y') is None