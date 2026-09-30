from docx_report_gen import (
    Report, StylesConfig, DocumentMetadata, HeadingStyle,
    CaptionStyle, ParagraphStyle, ListStyle, CodeStyle, QuoteStyle,
    b, i, u, s, sup, sub, color, highlight, f, link,
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
        quote=QuoteStyle(
            italic=True, left_indent=1.0, line_spacing=1.15,
        ),
        caption=CaptionStyle(prefix='Таблица', align='left'),
        image_caption=CaptionStyle(prefix='Рисунок', align='center'),
    )
    r = Report(config=config)

    r.title('Лабораторная работа №1')
    r.p('Выполнил: студент группы ИУ7-31', align='right')

    r.h1('1. Теоретическая часть')
    r.p('Известно, что ', f('E = mc'), sup('2'),
        ', что описывает ', b('эквивалентность'),
        ' массы и энергии. Молекула воды — H', sub('2'), 'O.')
    r.p('Это ', u('подчёркнутый'), ' текст, это — ', s('зачёркнутый'),
        ', это — ', color('красный', (200, 0, 0)),
        ', а это — ', highlight('жёлтый', 'yellow'),
        '. Ссылка: ', link('Wikipedia', 'https://wikipedia.org'), '.')

    r.h2('1.1. Цитата')
    r.quote('Энергия равна массе, умноженной на квадрат скорости света.')

    r.h2('1.2. Формула')
    r.f(r"\int_a^b f(x)\,dx = F(b) - F(a)", number=True)

    r.h1('2. Программная часть')
    r.code(
        'def energy(m, c=299_792_458):\n'
        '    return m * c ** 2\n'
    )

    r.save('lab_report.docx')


if __name__ == '__main__':
    main()