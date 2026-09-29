"""Usage example for docx-report-gen."""
from docx_report_gen import (
    Report, StylesConfig, HeadingStyle, CaptionStyle,
    ParagraphStyle, ListStyle, CodeStyle, QuoteStyle,
    b, i, f, link,
)


def main():
    config = StylesConfig(
        font='Times New Roman',
        size=12,
        align='left',
        margins=(2, 1, 2, 3),
        heading=HeadingStyle(align='left', color=(0, 0, 0)),
        heading_sizes=(16, 14, 13, 12, 12, 12),
        paragraph=ParagraphStyle(),
        formula=ParagraphStyle(align='center'),
        list=ListStyle(align='left', indent=0.75),
        code=CodeStyle(font='Consolas', size=10, background='F5F5F5'),
        quote=QuoteStyle(italic=True, indent=1.0),
        caption=CaptionStyle(prefix='Таблица', align='left'),
        image_caption=CaptionStyle(prefix='Рисунок', align='center'),
    )
    r = Report(config=config)

    r.title('Лабораторная работа №1')
    r.p('Выполнил: студент группы ИУ7-31', align='right')

    r.toc(title='Содержание')
    r.page_break()

    r.h1('1. Теоретическая часть')
    r.p('Известно, что ', f('E = mc^2'), ', что описывает ',
        b('эквивалентность'), ' массы и энергии. Подробнее — ',
        link('в статье', 'https://en.wikipedia.org/wiki/Mass–energy_equivalence'),
        '.')
    r.quote('Энергия равна массе, умноженной на квадрат скорости света.')

    r.h2('1.1. Свойства')
    r.ul([
        'Аддитивность',
        'Сохранение',
        ['в замкнутой системе', 'в открытой системе'],
    ])

    r.h2('1.2. Формулы')
    r.f(r"\int_a^b f(x)\,dx = F(b) - F(a)", number=True)
    r.f(r"\sum_{i=1}^n x_i", number=True)
    r.f(r"\alpha + \beta", align='left')   # без номера

    r.h1('2. Программная часть')
    r.code(
        'def energy(m, c=299_792_458):\n'
        '    """Rest energy of a mass."""\n'
        '    return m * c ** 2\n'
    )

    r.hr()
    r.table(
        [['Величина', 'Значение'], ['Масса', '1.25']],
        caption='Результаты измерений',
    )

    r.page_numbers(align='center', skip_first=True)
    r.header('Лабораторная работа №1')

    r.save('lab_report.docx')
    print('Готово: lab_report.docx')


if __name__ == '__main__':
    main()