"""Typical lab report — object API.

Shows headings, paragraphs with inline nodes, a numbered formula,
a table with caption, a numbered list, and page numbers.

Run:
    python examples/02_lab_report.py
Produces:
    lab_report.docx
"""
from docx_report_gen import (
    Report, StylesConfig, DocumentMetadata,
    HeadingStyle, ParagraphStyle, TableStyle, CaptionStyle,
    b, f, sup, sub, ref,
)


def main():
    config = StylesConfig(
        font='Times New Roman',
        size=12,
        align='left',
        margins=(2, 1, 2, 3),                # cm: top, right, bottom, left
        heading=HeadingStyle(align='left', color=(0, 0, 0)),
        paragraph=ParagraphStyle(line_spacing=1.5, space_after=6),
        table=TableStyle(align='center', header_align='center'),
        caption=CaptionStyle(prefix='Таблица', align='left'),
    )
    metadata = DocumentMetadata(
        author='Иван Иванов',
        title='Лабораторная работа №1',
        subject='Измерение ускорения свободного падения',
    )

    r = Report(config=config, metadata=metadata)

    r.title('Лабораторная работа №1')
    r.p('Выполнил: студент группы ИУ7-31', align='right')

    r.h1('1. Теоретическая часть')
    r.p('Известно, что ', f('E = mc'), sup('2'),
        ', что описывает ', b('эквивалентность'),
        ' массы и энергии. Молекула воды — H', sub('2'), 'O.')

    r.h2('1.1. Основная формула')
    r.f(r'\int_a^b f(x)\,dx = F(b) - F(a)', number=True)

    r.h1('2. Результаты измерений')
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
    )

    r.p('Смотрите таблицу ', ref('results'), ' для подробностей.')

    r.h2('2.1. Выводы')
    r.ul([
        'Значения согласуются с теорией',
        'Погрешность в пределах допустимого',
    ])

    r.page_numbers(align='center', skip_first=True)
    r.header('Лабораторная работа №1')

    r.save('lab_report.docx')
    print('Saved: lab_report.docx')


if __name__ == '__main__':
    main()