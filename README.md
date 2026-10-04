# docx-report-gen

Generate `.docx` reports from Python.

Two APIs: a **declarative object API** for full control, and an
**imperative writer API** for short scripts. Plugin system for
reusable extensions. Cross-references, formulas, TOC, page numbers —
all through native Word fields, so numbering stays correct when the
document is edited.

Reports can start from an empty document or from an existing `.docx`
file. When started from a file, all its styles, docDefaults, headers,
images and sections are preserved as-is; new content is appended
after it.

Built on top of [`python-docx`](https://python-docx.readthedocs.io/)
and [`math2docx`](https://github.com/py-pdf/math2docx).

- **Repository:** https://github.com/WarriorVortex/docx-report-gen
- **Issues:** https://github.com/WarriorVortex/docx-report-gen/issues
- **Python:** 3.9+
- **License:** MIT

---

## Status

Alpha, version `0.3.1`. The public API is stable within the `0.x`
series, but may change in minor releases.

---

## Installation

```bash
pip install docx-report-gen
```

From source:

```bash
pip install git+https://github.com/WarriorVortex/docx-report-gen.git
```

For development:

```bash
git clone https://github.com/WarriorVortex/docx-report-gen.git
cd docx-report-gen
pip install -e ".[dev]"
pytest
```

---

## Quick start

### Object API

```python
from docx_report_gen import Report, f, b, ref

r = Report()
r.title('Report')
r.h1('Introduction')
r.p('Formula: ', f('E = mc^2'), ', bold: ', b('important'))
r.table([['A', 'B'], [1, 2]], caption='Data', name='data')
r.p('See table ', ref('data'), '.')
r.save('report.docx')
```

### Writer API

`writer` is a lazy singleton. No `Report` instance is created until
the first block-level call. All functions can be imported flat.

```python
from docx_report_gen.writer import *

title('Report')
h1('Introduction')
p('Formula: ', f('E = mc^2'), ', bold: ', b('important'))
table([['A', 'B'], [1, 2]], caption='Data', name='data')
p('See table ', ref('data'), '.')
save('report.docx')
```

### Starting from an existing .docx

Both APIs can start from a file. The file becomes the base document:
its styles, docDefaults and content are preserved as-is. New content
is appended after it.

```python
from docx_report_gen import Report, TitlePagePlugin  # plugin optional

r = Report(source='Титульный лист.docx')
r.page_break()
r.h1('Введение')
r.p('Основной текст начинается со второй страницы.')
r.save('report.docx')
```

Or via the writer API:

```python
from docx_report_gen.writer import new, h1, p, save

new(source='Титульный лист.docx')
h1('Введение')
p('Основной текст.')
save('report.docx')
```

---

## Contents

- [Two APIs](#two-apis)
- [Starting from an existing document](#starting-from-an-existing-document)
- [Styles](#styles)
- [Metadata](#metadata)
- [Inline nodes](#inline-nodes)
- [Formulas and code](#formulas-and-code)
- [Tables and images](#tables-and-images)
- [Cross-references](#cross-references)
- [Table of contents and page furniture](#table-of-contents-and-page-furniture)
- [Plugins](#plugins)
- [Runtime configuration](#runtime-configuration)
- [API reference](#api-reference)
- [Examples](#examples)
- [Development](#development)
- [License](#license)

---

## Two APIs

Both APIs build the same document. Choose by context:

| Context | Recommended |
|---|---|
| Single script, top-to-bottom | `writer` (flat import) |
| Chained calls | `Report` |
| Multiple documents in one process | `Report` |
| Library that builds reports | `Report` |
| Interactive / REPL | `writer` |
| Threading, async, web | `Report` |

The object API is explicit. The writer API is convenient. They can
be mixed: `writer.attach(report)` installs an existing `Report` as
the singleton, `writer.detach()` returns it back.

### Object API

```python
from docx_report_gen import Report

r = Report()
r.h1('Title').p('Body').save('out.docx')   # chainable
```

Every block method returns the `Report` itself, so calls can chain.
Terminal operations (`save`) return `None`.

### Writer API

```python
from docx_report_gen.writer import *

h1('Title')          # creates the Report lazily
p('Body')
save('out.docx')
```

Every block function returns `None`. The module is imperative, not
chainable — flat-import scripts read better as a sequence of
statements.

**Session management:**

```python
from docx_report_gen.writer import (
    new, reset, attach, detach, current, has_session,
    set_source, set_document,
)

new()                             # fresh Report, drops previous session
new(config=my_config)             # fresh Report with config
new(source='base.docx')           # fresh Report from an existing .docx
reset()                           # drop session, no Report created
attach(existing_report)           # install an existing Report
detach()                          # return the Report, drop session
current()                         # access the current Report
has_session()                     # True if a Report exists
set_source('other.docx')          # replace the document mid-session
set_document(opened_docx)         # replace with a Document object
```

For a single document, `new()` is not required — the Report is
created on the first block call.

**Threading.** `writer` is a process-global singleton and is not
thread-safe. For concurrent document generation, use `Report`
directly.

---

## Starting from an existing document

The `source` parameter opens a `.docx` file as the base document.
This is the recommended way to include a title page, letterhead,
pre-styled template or any other preexisting content without losing
its formatting.

### Object API

```python
from docx_report_gen import Report

# From a path (str or Path)
r = Report(source='Титульный лист.docx')
r.page_break()
r.h1('Введение')
r.save('report.docx')

# From an already-opened Document
from docx import Document
opened = Document('title.docx')
r = Report(source=opened)

# Replace the document mid-session
r = Report()
r.h1('This will be discarded')
r.set_source('Титульный лист.docx')
r.h1('Введение')

# Replace with a Document object
from docx import Document
r.set_document(Document('template.docx'))

# Keep the source styles completely untouched
r.set_source('template.docx', apply_styles=False)
```

### Writer API

```python
from docx_report_gen.writer import (
    new, set_source, set_document, h1, p, save, current,
)

new(source='Титульный лист.docx')
h1('Введение')
save('report.docx')

# Replace mid-session
set_source('другой.docx')
h1('Новое введение')
save('report2.docx')

# From a Document object
from docx import Document
set_document(Document('template.docx'))
```

### What is preserved

Everything in the source file:

- All paragraphs, tables, images, embedded objects
- All styles, including style definitions not used by the content
- `docDefaults` (paragraph and run defaults)
- Headers, footers, page numbers
- Section properties: page size, orientation, margins
- Numbered and bulleted list definitions
- Document properties (core metadata)

### What changes

- The Report's `config` styles are re-applied to the document by
  default (`Normal`, `Heading 1..6`, `Title`, `ReportCode`, ...).
  This ensures that content added afterwards has the expected look.
  Pass `apply_styles=False` to skip and keep the source styles
  untouched.

- Bookmark, formula and table counters are reset. If the source
  already had numbered tables, the next one starts from 1.

### Save behavior

The document is written as-is. No transformation, no XML merge, no
`docDefaults` resolution. What you see in the source is what ends up
in the output, with new content appended.

```python
r = Report(source='source.docx')
r.h1('New content')
r.save('out.docx')
# out.docx contains the full source, plus New content at the end.
```

---

## Styles

All styling is configured once through a `StylesConfig` object.
Every element resolves its parameters through a three-level chain:

```
local argument → element subconfig → global StylesConfig → dataclass default
```

```python
from docx_report_gen import (
    Report, StylesConfig,
    HeadingStyle, CaptionStyle, ParagraphStyle,
    ListStyle, CodeStyle, QuoteStyle, TableStyle,
)

config = StylesConfig(
    font='Times New Roman',
    size=12,
    color=(0, 0, 0),
    align='justify',
    margins=(2, 1, 2, 3),                  # cm: top, right, bottom, left

    heading=HeadingStyle(align='left', color=(0, 0, 0), bold=True),
    heading_sizes=(18, 16, 14, 13, 12, 12),
    heading_overrides={2: HeadingStyle(align='center')},   # H2 centered

    title=HeadingStyle(size=20, align='center'),

    paragraph=ParagraphStyle(line_spacing=1.5, space_after=6),
    formula=ParagraphStyle(align='center'),

    list=ListStyle(align='left', left_indent=0.75),
    code=CodeStyle(font='Consolas', size=10, background='F5F5F5'),
    quote=QuoteStyle(italic=True, left_indent=1.0),

    table=TableStyle(
        align='center',
        col_aligns=('left', 'right'),
        header_align='center',
    ),

    caption=CaptionStyle(prefix='Table', align='left'),
    image_caption=CaptionStyle(prefix='Figure', align='center'),
)

r = Report(config=config)
```

**Local overrides at call sites:**

```python
r.h1('Left', align='left')
r.h1('Center', align='center')             # overrides config for this call
r.p('Justified paragraph', align='justify')
```

### Config classes

| Class | Purpose |
|---|---|
| `StylesConfig` | Root config, holds all subconfigs |
| `HeadingStyle` | Heading 1–6 and title |
| `ParagraphStyle` | Body paragraphs and formulas |
| `ListStyle` | Bullet and numbered lists |
| `CodeStyle` | Code blocks |
| `QuoteStyle` | Block quotes |
| `TableStyle` | Table alignment and column widths |
| `CaptionStyle` | Table and image captions |
| `ImageStyle` | Image alignment and width |
| `LayoutStyle` | Base class for paragraph-like styles |

### Conventions

- `align=None` in a subconfig means "inherit from the next source in
  the chain".
- `background=''` in `CodeStyle` disables shading. `None` means "not
  set here, try the next source".
- `heading_sizes` is a tuple; shorter tuples configure only the first
  N levels.

---

## Metadata

```python
from docx_report_gen import Report, DocumentMetadata

md = DocumentMetadata(
    author='Иван Иванов',
    title='Лабораторная работа №1',
    subject='Измерение g',
    keywords='физика, лабораторная',
    comments='Generated automatically',
    category='Отчёт',
    last_modified_by='docx-report-gen',
)
r = Report(metadata=md)
```

Metadata is written to `core_properties`. It is re-applied on every
`save()`, so you can change it mid-script:

```python
r.metadata.author = 'Другой автор'
r.save('out.docx')     # core_properties.author is now 'Другой автор'
```

When a Report starts from a source file, the source's metadata is
preserved unless explicitly overwritten.

---

## Inline nodes

Inline nodes are values, not strings. Construct them with factory
functions and pass them into `p(...)` or `quote(...)`:

```python
from docx_report_gen import (
    b, i, u, s, sup, sub, color, highlight, code, f, link, ref,
)

r.p('Text with ', b('bold'), ', ', i('italic'), ', ', u('underline'), '.')
r.p('Chem: H', sub('2'), 'O. Math: x', sup('2'), '.')
r.p('Red: ', color('red text', (255, 0, 0)))
r.p('Marked: ', highlight('important', 'yellow'))
r.p('Formula: ', f('E = mc^2'))
r.p('Inline code: ', code('print'))
r.p('Link: ', link('Wikipedia', 'https://en.wikipedia.org'))
r.p('See ', ref('results'), '.')
```

| Factory | Renders as |
|---|---|
| `b(text)` | Bold |
| `i(text)` | Italic |
| `u(text)` | Underline |
| `s(text)` | Strikethrough |
| `sup(text)` | Superscript |
| `sub(text)` | Subscript |
| `color(text, rgb)` | Colored text, `rgb` is `(r, g, b)` in 0..255 |
| `highlight(text, name)` | Highlighted text |
| `code(text)` | Inline monospace |
| `f(latex)` | Inline formula |
| `link(text, url)` | Hyperlink |
| `ref(name)` | Cross-reference to a bookmarked element |

**Highlight color names:** `yellow`, `green`, `cyan`, `magenta`,
`blue`, `red`, `darkGreen`, `darkCyan`, `darkMagenta`, `lightGray`,
`darkGray`, `black`, `white`. Names are case-sensitive (they are WML
values). A `WD_COLOR_INDEX` member is also accepted.

---

## Formulas and code

Both have an inline form and a block form under the same name.

| Context | Formula | Code |
|---|---|---|
| Inline | `f('E = mc^2')` | `code('print')` |
| Block (writer) | `f.block('E = mc^2')` | `code.block('def f(): ...')` |
| Block (object) | `r.f('E = mc^2')` | `r.code('def f(): ...')` |

A bare `f(...)` or `code(...)` in the writer API returns an inline
node — it does **not** modify the document. To add content, use the
`.block(...)` method.

### Block formulas with numbers

```python
r.f(r'\int_0^1 x^2 \, dx = \frac{1}{3}', number=True)
```

Numbered formulas get a right-aligned counter `(1)`, `(2)`, ... The
counter is per-`Report` and resets between Reports. Unnumbered
formulas do not consume a number.

### Block code

```python
r.code(
    'def energy(m, c=299_792_458):\n'
    '    return m * c ** 2\n',
)
```

Each line becomes its own paragraph, so long blocks break across
pages naturally. Empty lines become a paragraph with a single space.
The `language` argument is accepted but does not affect rendering —
Word has no built-in syntax highlighting.

---

## Tables and images

### Tables

```python
r.table(
    [['A', 'B'], [1, 2], [3, 4]],
    caption='Measurements',
    name='data',                       # for ref('data')
    col_widths=(4.0, 6.0),             # cm, or single number for all
    col_aligns=('left', 'right'),
    header_align='center',
)
```

Captions use a `SEQ Table` field. Numbering is done by Word, so it
survives reordering. If `name` is given, a bookmark is created for
cross-referencing.

### Merged cells

```python
r.table([['A', 'B', 'C'], ['x', 'y', 'z']])
r.merge_row(0, 0, 2, text='merged')   # merge A..C in row 0
r.merge_col(0, 0, 2, text='column')   # merge rows 0..2 in column 0
r.merge_cells(0, 0, 1, 1, text='block')
```

Merges apply to the most recently created table.

### Images

```python
r.img('plot.png', caption='Dependency y(x)', name='plot', width=10.0)
```

- `width` in centimeters (a `float`) or a python-docx `Length` object
  (e.g. `Inches(4)`).
- Captions use a `SEQ Figure` field.
- `name` creates a bookmark for cross-referencing.
- Missing files raise `FileNotFoundError`.

---

## Cross-references

```python
r.table(..., caption='Data', name='results')
r.img('plot.png', caption='Plot', name='plot')

r.p('See table ', ref('results'), ' and figure ', ref('plot'), '.')
```

Cross-references render as Word `REF` fields. Word fills in the
actual number and updates it when the target renumbers. In Word,
press F9 to update all fields; in LibreOffice, use
Tools → Update → Update All.

The name passed to `ref()` must match the `name` argument of a
`table(...)` or `img(...)` call. Names must not contain whitespace.

---

## Table of contents and page furniture

```python
r.toc(title='Содержание', levels='1-2')
r.update_toc()                        # mark all fields dirty for Word
r.header('Report generated automatically')
r.footer('Page footer text')
r.page_numbers(align='center', skip_first=True)
r.page_break()
r.hr()
```

- `toc()` inserts a Word `TOC` field. Word updates it on open (or
  with F9).
- `update_toc()` sets the document-wide `updateFields` flag in
  `settings.xml` and marks every field dirty. Use it near the end of
  a script if the document has a TOC.
- `page_numbers(skip_first=True)` suppresses the header and footer
  on the first page — useful for title pages.

When a Report starts from a source file that already has headers or
footers, calls to `header()`, `footer()` or `page_numbers()`
overwrite them for the entire document.

---

## Plugins

A plugin extends `Report` with custom block methods, inline nodes,
or lifecycle hooks.

```python
from docx_report_gen import Plugin
from docx_report_gen.inline import Inline


class Boxed(Inline):
    def __init__(self, text):
        self.text = text
    def render(self, para):
        run = para.add_run(f'[{self.text}]')
        run.italic = True


class LayoutPlugin(Plugin):
    name = 'layout'

    def setup(self, report):
        # Block method — becomes writer.centered(...) and
        # report.centered(...) via __getattr__.
        self.registry.block('centered', self._centered)
        # Inline node factory — becomes writer.boxed(...) and
        # report.boxed(...).
        self.registry.inline('boxed', Boxed)

    def before_save(self, report, path):
        report.header('Generated automatically')

    def _centered(self, report, text):
        report.p(text, align='center')

    def note(self, text):
        """Direct method — uses self.report."""
        self.report.p('Note: ', text)
```

### Registering plugins

Two scopes:

**Global** — applies to every future `Report`:

```python
from docx_report_gen.writer import register_plugin

register_plugin(LayoutPlugin())
```

**Local** — this document only:

```python
from docx_report_gen import Report
r = Report(plugins=[LayoutPlugin()])
```

### Using plugin methods

Block-registered methods are reachable through `__getattr__`:

```python
import docx_report_gen.writer as writer

writer.centered('Centered line')       # via writer
r.centered('Centered line')            # via Report
```

Direct methods (those using `self.report`) are reached through
`use_plugin(...)`:

```python
from docx_report_gen.writer import use_plugin

use_plugin('layout').note('Important observation')
use_plugin(LayoutPlugin).note('Again')          # by class
use_plugin(some_instance).note('And again')     # by instance
```

With a class or instance, `use_plugin` registers the plugin
automatically if it is not yet attached to the current session. With
a name string, it looks up an existing plugin and raises `KeyError`
if the name is not registered.

### Plugin lifecycle

Override any of these methods on `Plugin`:

| Hook | When |
|---|---|
| `setup(report)` | Plugin attached to a Report |
| `before_save(report, path)` | Before the document is written |
| `after_save(report, path)` | After the document is written |
| `before_close(report)` | Before the plugin is detached |
| `after_close(report)` | After the plugin is detached |

`Report.close()` runs the close hooks and clears the local registry.

---

## Runtime configuration

### Styles

Change the whole config at once — Word styles are re-applied
immediately:

```python
r.set_config(StylesConfig(font='Arial'))
```

Mutate in place and opt in to re-applying:

```python
r.config.heading.align = 'center'
r.apply_styles()
```

Note: paragraph-level overrides from earlier calls — e.g.
`r.h1('X', align='right')` — are preserved. Only the underlying Word
style definitions are re-derived.

### Metadata

```python
r.set_metadata(DocumentMetadata(author='Late Author'))
r.save('out.docx')                      # core_properties updated on save

r.metadata.author = 'In-place change'
r.save('out.docx')                      # also picked up

r.apply_metadata()                      # flush to core_properties now
```

`save()` re-applies metadata automatically. `apply_metadata()` is
only needed if you want to inspect `core_properties` before saving.

### Replacing the document

See [Starting from an existing document](#starting-from-an-existing-document)
for the full guide.

```python
r.set_source('template.docx')           # replace, re-apply styles
r.set_source('template.docx', apply_styles=False)  # keep styles as-is
r.set_document(opened_docx)             # from a Document object
```

---

## API reference

### Package top-level

```python
from docx_report_gen import (
    # main classes
    Report, Plugin, PluginsRegistry,
    StylesConfig, DocumentMetadata,
    # style configs
    HeadingStyle, CaptionStyle, ParagraphStyle, ImageStyle,
    ListStyle, CodeStyle, QuoteStyle, TableStyle, LayoutStyle,
    # inline factories
    b, i, u, s, sup, sub, color, highlight, code, f, link, ref,
    # submodules
    docx, writer,
)
```

### `Report`

| Method | Purpose |
|---|---|
| **Construction** | |
| `Report(config=, metadata=, plugins=, source=)` | Create a Report |
| **Document replacement** | |
| `set_source(path, apply_styles=True)` | Replace with contents of a .docx |
| `set_document(doc, apply_styles=True)` | Replace with a Document object |
| **Structure** | |
| `title(text, align=None)` | Title paragraph |
| `h1..h6(text, align=None)` | Headings level 1–6 |
| `page_break()` | Page break |
| `hr()` | Horizontal rule |
| **Content** | |
| `p(*parts, **layout)` | Paragraph from strings and inline nodes |
| `f(latex, align=None, number=False)` | Block formula |
| `quote(*parts, **layout)` | Block quote |
| `ul(items, align=None)` | Bulleted list |
| `ol(items, align=None)` | Numbered list |
| `code(text, language=None, **layout)` | Code block |
| `table(data, caption=None, name=None, **opts)` | Table |
| `img(path, caption=None, name=None, width=None, align=None)` | Image |
| `merge_cells(r1, c1, r2, c2, text=None)` | Merge cells |
| `merge_row(row, c1, c2, text=None)` | Merge row cells |
| `merge_col(col, r1, r2, text=None)` | Merge column cells |
| **Page furniture** | |
| `toc(title=None, levels='1-3')` | Table of contents |
| `update_toc()` | Mark fields dirty for Word |
| `header(text, align='center')` | Header |
| `footer(text=None, align='center')` | Footer |
| `page_numbers(align='center', skip_first=True)` | Page numbers |
| **Runtime configuration** | |
| `set_config(config)` | Replace config, re-apply styles |
| `apply_styles()` | Re-apply config after in-place edits |
| `set_metadata(metadata)` | Replace metadata |
| `apply_metadata()` | Flush metadata to `core_properties` |
| `style(name)` | Access python-docx style |
| **Lifecycle** | |
| `save(path)` | Write the document |
| `close()` | Run plugin close hooks, clear registry |

**Attributes:** `doc`, `config`, `metadata`, `plugins`.

### `docx_report_gen.writer`

| Function | Purpose |
|---|---|
| **Session** | |
| `new(config=None, metadata=None, plugins=None, source=None)` | Fresh Report |
| `reset()` | Drop session |
| `attach(report)` | Install existing Report |
| `detach()` | Return the Report, drop session |
| `current()` | Access the Report (creates one) |
| `has_session()` | Session is active |
| **Document replacement** | |
| `set_source(path, apply_styles=True)` | Replace document with .docx contents |
| `set_document(doc, apply_styles=True)` | Replace with a Document object |
| **Config / metadata** | |
| `config()` | Current `StylesConfig` |
| `set_config(cfg)` | Replace config, re-apply |
| `apply_styles()` | Re-apply after in-place edits |
| `metadata()` | Current `DocumentMetadata` |
| `set_metadata(md)` | Replace metadata |
| `apply_metadata()` | Flush to `core_properties` now |
| `style(name)` | python-docx style object |
| **Plugins** | |
| `register_plugin(p)` | Global registration |
| `unregister_plugin(p)` | Remove global plugin |
| `plugins()` | Current Report's local registry |
| `use_plugin(name \| class \| instance)` | Obtain a plugin handle |
| `block(name, handler)` | Register block method locally |
| `inline_node(name, factory)` | Register inline factory locally |
| **Structure** | |
| `title`, `h1`–`h6`, `page_break`, `hr` | Same as `Report` |
| **Content** | |
| `p`, `quote`, `ul`, `ol`, `table`, `img` | Same as `Report` |
| `merge_cells`, `merge_row`, `merge_col` | Same as `Report` |
| **Accessors** | |
| `f(latex)` / `f.block(latex, ...)` | Inline / block formula |
| `code(text)` / `code.block(text, ...)` | Inline / block code |
| **Page furniture** | |
| `toc`, `update_toc`, `header`, `footer`, `page_numbers` | Same as `Report` |
| **Lifecycle** | |
| `save(path)` | Write, keep session |
| `close()` | Close plugins, drop session |
| **Inline factories** | |
| `b, i, u, s, sup, sub, color, highlight, link, ref` | Same as top-level |

### `docx_report_gen.docx`

Re-exports of python-docx primitives and enums:

```python
from docx_report_gen import docx

docx.DocxDocument        # the real python-docx Document class
docx.Paragraph
docx.Table
docx.Cm, docx.Pt, docx.Inches, docx.Mm, docx.Emu
docx.RGBColor
docx.WD_ALIGN_PARAGRAPH, docx.WD_COLOR_INDEX, ...
docx.to_twips(value, unit='cm')    # length -> twips
```

---

## Examples

See [`examples/`](examples/):

| File | Shows |
|---|---|
| `01_minimal.py` | Three-line script |
| `02_lab_report.py` | Object API, styles, formulas, tables, references |
| `03_writer_basic.py` | Writer flat import |
| `04_writer_session.py` | `new`, `attach`, `detach` |
| `05_plugins.py` | Plugin with block and direct methods |
| `06_full_report.py` | Full report with TOC, page numbers, all features |

Run any example from the repository root:

```bash
python examples/01_minimal.py
```

---

## Development

```bash
pip install -e ".[dev]"
pytest -v                          # all tests
pytest --cov --cov-report=html     # coverage report
mypy src/docx_report_gen --strict  # type check
```

Target coverage: 80%+.

---

## License

MIT. See [LICENSE](LICENSE).

---

## Repository

https://github.com/WarriorVortex/docx-report-gen