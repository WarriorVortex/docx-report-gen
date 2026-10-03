"""Full report — every feature at once.

Headings, paragraphs with inline nodes, block formulas with numbers,
TOC, page numbers, header, optional image, table with caption,
cross-references, code block, nested lists.

The image is optional. If examples/assets/sample.png exists, it is
included; otherwise the image block is skipped.

Run:
    python examples/06_full_report.py
Produces:
    full_report.docx
"""
from pathlib import Path

from docx_report_gen import (
    Report, StylesConfig, DocumentMetadata,
    HeadingStyle, CaptionStyle, ParagraphStyle,
    ListStyle, CodeStyle, QuoteStyle, TableStyle,
    b, i, u, s, sup, color, highlight, f, link, ref, code as inline_code,
)


HERE = Path(__file__).resolve().parent
SAMPLE_IMAGE = HERE / 'assets' / 'sample.png'


def main():
    config = StylesConfig(
        font='Times New Roman',
        size=12,
        align='left',
        margins=(2, 1, 2, 3),
        heading=HeadingStyle(align='left', color=(0, 0, 0)),
        paragraph=ParagraphStyle(line_spacing=1.5, space_after=6),
        list=ListStyle(align='left', left_indent=0.75),
        code=CodeStyle(font='Consolas', size=10, background='F5F5F5'),
        quote=QuoteStyle(italic=True, left_indent=1.0),
        table=TableStyle(align='center', header_align='center'),
        caption=CaptionStyle(prefix='Таблица', align='left'),
    )
    metadata = DocumentMetadata(
        author='WarriorVortex',
        title='Full report demo',
        subject='docx-report-gen capabilities',
        keywords='docx, report, python',
    )

    r = Report(config=config, metadata=metadata)

    r.title('Итоговый отчёт')
    r.p('Демонстрация возможностей docx-report-gen', align='right')

    r.toc(title='Содержание', levels='1-2')
    r.page_break()

    # ---------- Introduction ----------
    r.h1('1. Введение')
    r.p('Известно, что ', f('E = mc'), sup('2'), ', что описывает ',
        b('эквивалентность'), ' массы и энергии. См. ',
        link('Wikipedia', 'https://en.wikipedia.org'), '.')
    r.p('Разные форматы: ', i('курсив'), ', ', u('подчёркнутый'), ', ',
        s('зачёркнутый'), ', ', color('красный', (200, 0, 0)), ', ',
        highlight('жёлтый', 'yellow'), '.')
    r.p('Инлайн-код: ', inline_code('print'), ', и встроенная формула: ',
        f('a^2 + b^2 = c^2'), '.')

    r.quote('Энергия равна массе, умноженной на квадрат скорости света.')

    # ---------- Formulas ----------
    r.h2('1.1. Формулы')
    r.f(r'\int_0^1 x^2 \, dx = \frac{1}{3}', number=True)
    r.f(r'\sum_{i=1}^{n} x_i', number=True)

    # ---------- Results ----------
    r.h1('2. Результаты')

    if SAMPLE_IMAGE.exists():
        r.img(str(SAMPLE_IMAGE), caption='Зависимость y(x)',
              name='plot', width=10.0)

    r.p('Результаты измерений приведены в таблице ', ref('results'), '.')

    r.table(
        [
            ['Величина', 'Значение', 'Погрешность'],
            ['Масса, кг', '1.25', '±0.01'],
            ['Скорость, м/с', '340', '±2'],
            ['Ускорение, м/с²', '9.81', '±0.01'],
        ],
        caption='Результаты измерений',
        name='results',
        col_widths=(5.0, 3.0, 3.0),
        col_aligns=('left', 'right', 'right'),
    )

    r.h2('2.1. Обсуждение')
    r.p('Как видно из таблицы ', ref('results'),
        ', значения согласуются с теорией.')

    # ---------- Software part ----------
    r.h1('3. Программная часть')
    r.code(
        'def energy(m, c=299_792_458):\n'
        '    """Rest energy of a mass."""\n'
        '    return m * c ** 2\n'
    )

    r.h2('3.1. Шаги воспроизведения')
    r.ul([
        'Подготовить входные данные',
        'Запустить вычисления',
        ['Проверить размерность', 'Проверить знак'],
        'Записать результаты',
    ])

    r.h2('3.2. Список параметров')
    r.ol([
        'Первый параметр',
        'Второй параметр',
        'Третий параметр',
    ])

    # ---------- Page furniture ----------
    r.page_numbers(align='center', skip_first=True)
    r.header('Отчёт сгенерирован автоматически')
    r.update_toc()

    r.save('full_report.docx')
    print('Saved: full_report.docx')


if __name__ == '__main__':
    main()