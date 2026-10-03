"""Plugin example.

Two styles of plugin extension coexist:

- block registration (self.registry.block) — reachable as
  writer.<name>(...) and report.<name>(...).
- direct methods using self.report — reachable through
  writer.use_plugin(...) or report.plugins.get_plugin(...).

Run:
    python examples/05_plugins.py
Produces:
    plugin_demo.docx
"""
import docx_report_gen.writer as writer
from docx_report_gen import Plugin, StylesConfig
from docx_report_gen.writer import (
    new, h1, p, save, use_plugin, register_plugin, f,
)


class LayoutPlugin(Plugin):
    """Adds a `centered` block method and a `note` direct method."""

    name = 'layout'

    def setup(self, report):
        # Block registration — becomes writer.centered(...) and
        # report.centered(...) via __getattr__.
        self.registry.block('centered', self._centered)
        # Header applied before every save.
        report.header('Отчёт с плагином')

    def _centered(self, report, text):
        report.p(text, align='center')

    def note(self, text):
        """Direct method — uses self.report, no arguments needed."""
        self.report.p('Замечание: ', text, align='left')


def main():
    # Global registration: applies to every Report created afterwards.
    register_plugin(LayoutPlugin())

    new(config=StylesConfig())

    h1('1. Обычный текст')
    p('Формула: ', f('E = mc^2'))

    h1('2. Через block-регистрацию')
    writer.centered('Этот абзац по центру')

    h1('3. Через direct-метод')
    use_plugin('layout').note('важное наблюдение')
    use_plugin(LayoutPlugin).note('тот же плагин, найден по классу')

    save('plugin_demo.docx')
    print('Saved: plugin_demo.docx')


if __name__ == '__main__':
    main()