"""End-to-end test: build a full report and verify the artifacts.

This test uses every major feature together — headings, paragraphs
with inline nodes, lists, code, table with caption, image, block
formulas, TOC, page numbers — and checks the resulting .docx.
"""
from docx import Document

from docx_report_gen import (
    Report, StylesConfig, DocumentMetadata,
    HeadingStyle, CaptionStyle, ParagraphStyle,
    ListStyle, CodeStyle, QuoteStyle, TableStyle,
    b, i, u, s, sup, sub, color, highlight, f, link, ref,
)

from ._helpers import (
    all_text, bookmark_names, count_instr_fields, count_omath,
    hyperlink_targets, list_parts,
)


def _build_full_report(config, metadata, png_image):
    r = Report(config=config, metadata=metadata)

    r.title('Итоговый отчёт')
    r.p('Выполнил: студент', align='right')

    r.toc(title='Содержание', levels='1-2')
    r.page_break()

    r.h1('1. Введение')
    r.p('Известно, что ', f('E = mc'), sup('2'),
        ', что описывает ', b('эквивалентность'),
        ' массы и энергии. См. ', link('Wikipedia', 'https://en.wikipedia.org'),
        '.')
    r.p('Небольшая демонстрация форматов: ',
        i('курсив'), ', ', u('подчёркнутое'), ', ',
        s('зачёркнутое'), ', ', color('красный', (200, 0, 0)), ', ',
        highlight('жёлтый', 'yellow'), '.')

    r.quote('Энергия равна массе, умноженной на квадрат скорости света.')

    r.h2('1.1. Формулы')
    r.f(r'\int_0^1 x^2 \, dx = \frac{1}{3}', number=True)
    r.f(r'\sum_{i=1}^{n} x_i', number=True)

    r.h1('2. Результаты')
    r.img(png_image, caption='График зависимости', name='plot', width=6.0)

    r.table(
        [
            ['Величина', 'Значение', 'Погрешность'],
            ['Масса, кг', '1.25', '±0.01'],
            ['Скорость, м/с', '340', '±2'],
        ],
        caption='Результаты измерений',
        name='results',
        col_widths=(5.0, 3.0, 3.0),
        col_aligns=('left', 'right', 'right'),
        header_align='center',
    )

    r.h2('2.1. Обсуждение')
    r.p('Как видно из таблицы ', ref('results'),
        ' и рисунка ', ref('plot'), ', значения согласуются.')

    r.h1('3. Программная часть')
    r.code('def energy(m, c=299_792_458):\n    return m * c ** 2')

    r.ul(['Первый пункт', 'Второй пункт', ['Подпункт 1', 'Подпункт 2']])

    r.page_numbers(align='center', skip_first=True)
    r.header('Отчёт сгенерирован автоматически')
    return r


# ---------- artifacts ----------

def test_full_report_can_be_built_and_saved(tmp_path, png_image):
    config = StylesConfig(
        font='Times New Roman',
        size=12,
        margins=(2, 1, 2, 3),
        heading=HeadingStyle(align='left', color=(0, 0, 0)),
        paragraph=ParagraphStyle(line_spacing=1.5, space_after=6),
        list=ListStyle(align='left', left_indent=0.75),
        code=CodeStyle(font='Consolas', size=10, background='F5F5F5'),
        quote=QuoteStyle(italic=True, left_indent=1.0),
        table=TableStyle(align='center'),
        caption=CaptionStyle(prefix='Таблица', align='left'),
    )
    metadata = DocumentMetadata(
        author='Тестовый Автор',
        title='Итоговый отчёт',
        subject='Интеграционный тест',
    )
    r = _build_full_report(config, metadata, png_image)
    path = tmp_path / 'full.docx'
    r.save(str(path))
    assert path.exists()
    assert path.stat().st_size > 0


def test_full_report_reopens_via_python_docx(tmp_path, png_image):
    r = _build_full_report(StylesConfig(), DocumentMetadata(), png_image)
    path = tmp_path / 'full.docx'
    r.save(str(path))

    doc = Document(str(path))
    assert len(doc.paragraphs) > 10
    assert len(doc.tables) == 1
    assert len(doc.inline_shapes) == 1


def test_full_report_metadata_round_trip(tmp_path, png_image):
    metadata = DocumentMetadata(
        author='Тестовый Автор',
        title='Отчёт №1',
        subject='Проверка',
        keywords='тест, интеграция',
    )
    r = _build_full_report(StylesConfig(), metadata, png_image)
    path = tmp_path / 'full.docx'
    r.save(str(path))

    doc = Document(str(path))
    assert doc.core_properties.author == 'Тестовый Автор'
    assert doc.core_properties.title == 'Отчёт №1'
    assert doc.core_properties.subject == 'Проверка'
    assert 'тест' in doc.core_properties.keywords


def test_full_report_contains_all_sections(tmp_path, png_image):
    r = _build_full_report(StylesConfig(), DocumentMetadata(), png_image)
    path = tmp_path / 'full.docx'
    r.save(str(path))

    text = all_text(path)
    assert 'Итоговый отчёт' in text
    assert '1. Введение' in text
    assert '2. Результаты' in text
    assert '3. Программная часть' in text
    assert 'Результаты измерений' in text
    assert 'График зависимости' in text


def test_full_report_has_three_omath_formulas(tmp_path, png_image):
    r = _build_full_report(StylesConfig(), DocumentMetadata(), png_image)
    path = tmp_path / 'full.docx'
    r.save(str(path))

    # Two block formulas + one inline formula in the introduction = 3
    assert count_omath(path) == 3


def test_full_report_seq_fields(tmp_path, png_image):
    r = _build_full_report(StylesConfig(), DocumentMetadata(), png_image)
    path = tmp_path / 'full.docx'
    r.save(str(path))

    assert count_instr_fields(path, 'SEQ Table') == 1
    assert count_instr_fields(path, 'SEQ Figure') == 1


def test_full_report_ref_fields(tmp_path, png_image):
    r = _build_full_report(StylesConfig(), DocumentMetadata(), png_image)
    path = tmp_path / 'full.docx'
    r.save(str(path))

    assert count_instr_fields(path, 'REF _Ref_results') == 1
    assert count_instr_fields(path, 'REF _Ref_plot') == 1


def test_full_report_toc_field_present(tmp_path, png_image):
    r = _build_full_report(StylesConfig(), DocumentMetadata(), png_image)
    path = tmp_path / 'full.docx'
    r.save(str(path))

    assert count_instr_fields(path, 'TOC') == 1


def test_full_report_bookmarks_created(tmp_path, png_image):
    r = _build_full_report(StylesConfig(), DocumentMetadata(), png_image)
    path = tmp_path / 'full.docx'
    r.save(str(path))

    names = bookmark_names(path)
    assert '_Ref_plot' in names
    assert '_Ref_results' in names


def test_full_report_hyperlink_registered(tmp_path, png_image):
    r = _build_full_report(StylesConfig(), DocumentMetadata(), png_image)
    path = tmp_path / 'full.docx'
    r.save(str(path))

    targets = hyperlink_targets(path)
    assert 'https://en.wikipedia.org' in targets


def test_full_report_has_header_and_footer_parts(tmp_path, png_image):
    r = _build_full_report(StylesConfig(), DocumentMetadata(), png_image)
    path = tmp_path / 'full.docx'
    r.save(str(path))

    parts = list_parts(path)
    header_parts = [p for p in parts if p.startswith('word/header')]
    footer_parts = [p for p in parts if p.startswith('word/footer')]
    assert header_parts, 'no header part'
    assert footer_parts, 'no footer part'


def test_full_report_page_break_present(tmp_path, png_image):
    r = _build_full_report(StylesConfig(), DocumentMetadata(), png_image)
    path = tmp_path / 'full.docx'
    r.save(str(path))

    from ._helpers import xml_part
    xml = xml_part(path, 'word/document.xml')
    W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    breaks = [
        br for br in xml.iter(f'{{{W}}}br')
        if br.get(f'{{{W}}}type') == 'page'
    ]
    assert breaks


# ---------- repeatability ----------

def test_full_report_save_twice(tmp_path, png_image):
    r = _build_full_report(StylesConfig(), DocumentMetadata(), png_image)
    p1 = tmp_path / 'a.docx'
    p2 = tmp_path / 'b.docx'
    r.save(str(p1))
    r.save(str(p2))
    assert p1.exists()
    assert p2.exists()
    # Both files open cleanly
    Document(str(p1))
    Document(str(p2))


def test_two_reports_do_not_share_state(tmp_path, png_image):
    r1 = _build_full_report(StylesConfig(), DocumentMetadata(), png_image)
    r2 = _build_full_report(StylesConfig(), DocumentMetadata(), png_image)

    p1 = tmp_path / 'r1.docx'
    p2 = tmp_path / 'r2.docx'
    r1.save(str(p1))
    r2.save(str(p2))

    # Both reports must have (1) as the first formula number, not (1)/(2)
    t1 = all_text(p1)
    t2 = all_text(p2)
    assert '(1)' in t1
    assert '(1)' in t2


def test_full_report_bookmark_ids_unique(tmp_path, png_image):
    """Two books (table, image) get distinct ids, both are present."""
    r = _build_full_report(StylesConfig(), DocumentMetadata(), png_image)
    path = tmp_path / 'full.docx'
    r.save(str(path))

    from ._helpers import xml_part
    xml = xml_part(path, 'word/document.xml')
    W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    ids = [
        el.get(f'{{{W}}}id')
        for el in xml.findall(f'.//{{{W}}}bookmarkStart')
    ]
    # Word requires unique ids even when names differ.
    assert len(ids) == len(set(ids))