"""Usage example for docx-report-gen."""
from docx_report_gen import (
    Report, StylesConfig, DocumentMetadata, HeadingStyle,
    CaptionStyle, ParagraphStyle, ListStyle, CodeStyle, QuoteStyle,
    TableStyle, b, i, u, s, sup, sub, color, highlight, f, link, ref,
)


def main():
    config = StylesConfig(
        font='Times New Roman',
        size=12,
        align='left',
        margins=(2, 1, 2, 3),
        heading=HeadingStyle(align='left', color=(0, 0, 0)),
        heading_sizes=(16, 14, 13, 12, 12, 12),
        paragraph=ParagraphStyle(
            line_spacing=1.5,
            space_after=6,
            first_line_indent=1.25,
        ),
        formula=ParagraphStyle(
            align='center', space_before=6, space_after=6,
        ),
        list=ListStyle(align='left', left_indent=0.75),
        code=CodeStyle(
            font='Consolas', size=10, background='F5F5F5',
            line_spacing=1.0, space_after=0,
        ),
        quote=QuoteStyle(italic=True, left_indent=1.0),
        table=TableStyle(
            align='center',
            col_widths=(5.0, 3.0, 3.0),
            col_aligns=('left', 'right', 'center'),
            header_align='center',
        ),
        caption=CaptionStyle(prefix='Таблица', align='left'),
        image_caption=CaptionStyle(prefix='Рисунок', align='center'),
    )
    metadata = DocumentMetadata(
        author='Иван Иванов',
        title='Лабораторная работа №1',
        subject='Эквивалентность массы и энергии',
        keywords='физика, лабораторная',
        category='Отчёт',
    )
    r = Report(config=config, metadata=metadata)

    r.title('Лабораторная работа №1')
    r.p('Выполнил: студент группы ИУ7-31', align='right')

    r.toc(title='Содержание', levels='1-2')
    r.page_break()

    r.h1('1. Теоретическая часть')
    r.p('Известно, что ', f('E = mc'), sup('2'),
        ', что описывает ', b('эквивалентность'),
        ' массы и энергии. Смотрите рисунок ', ref('plot'),
        ' и таблицу ', ref('results'), '.')

    r.h1('2. Результаты')
    r.img('plot.png', caption='Зависимость y(x)',
          name='plot', width=12)
    r.table(
        [
            ['Величина', 'Значение', 'Погрешность'],
            ['Масса, кг', '1.25', '±0.01'],
            ['Скорость, м/с', '340', '±2'],
        ],
        caption='Результаты измерений',
        name='results',
    )

    r.h1('3. Обсуждение')
    r.p('Как видно из таблицы ', ref('results'),
        ', значения согласуются с теорией, '
        'представленной на рисунке ', ref('plot'), '.')

    r.page_numbers(align='center', skip_first=True)
    r.header('Лабораторная работа №1')

    r.save('lab_report.docx')
    print('Готово: lab_report.docx')


if __name__ == '__main__':
    main()