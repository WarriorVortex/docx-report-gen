"""Same report via the writer API — flat import.

Writer is a lazy singleton: no Report instance is created until the
first block-level call. Bare `f(...)` returns an inline node; use
`f.block(...)` for a standalone formula paragraph.

Run:
    python examples/03_writer_basic.py
Produces:
    writer_basic.docx
"""
from docx_report_gen.writer import (
    title, h1, h2, p, ul, table, save,
    page_numbers, header,
    f, b, sup, sub, code, ref,
)


def main():
    title('Лабораторная работа №1')
    h1('1. Введение')
    p('Формула: ', f('E = mc^2'), ', жирным: ', b('важно'), '.')
    p('Индекс: H', sub('2'), 'O, степень: x', sup('2'), '.')
    p('Функция ', code('print'), ' выводит текст.')

    h2('1.1. Основной результат')
    f.block(r'\int_a^b f(x)\,dx', number=True)

    h1('2. Данные')
    table(
        [['A', 'B'], [1, 2], [3, 4]],
        caption='Измерения',
        name='data',
    )
    p('См. таблицу ', ref('data'), '.')

    ul(['Первый пункт', 'Второй пункт'])

    page_numbers(align='center', skip_first=True)
    header('Отчёт сгенерирован автоматически')

    save('writer_basic.docx')
    print('Saved: writer_basic.docx')


if __name__ == '__main__':
    main()