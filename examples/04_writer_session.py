"""Writer session management — new, attach, detach.

Demonstrates three patterns:

1. new() to start a fresh document with custom config.
2. attach() to work on a Report created elsewhere.
3. detach() to hand the Report back to object-style code.

Run:
    python examples/04_writer_session.py
Produces:
    session_1.docx, session_2.docx, session_3.docx
"""
from docx_report_gen import (
    Report, StylesConfig, HeadingStyle, DocumentMetadata,
)
from docx_report_gen.writer import (
    new, attach, detach, has_session,
    title, h1, p, save, f,
)


def main():
    # ---------- 1. new() with custom config ----------
    new(
        config=StylesConfig(font='Georgia', heading=HeadingStyle(align='left')),
        metadata=DocumentMetadata(author='Первый'),
    )
    title('Отчёт №1')
    h1('Первый раздел')
    p('Формула: ', f('E = mc^2'))
    save('session_1.docx')

    # ---------- 2. attach() to a Report created outside ----------
    external = Report(
        config=StylesConfig(font='Arial'),
        metadata=DocumentMetadata(author='Второй'),
    )
    attach(external)
    title('Отчёт №2')
    h1('Первый раздел второго отчёта')
    p('Формула: ', f('a^2 + b^2 = c^2'))
    save('session_2.docx')

    # ---------- 3. detach() and continue with object API ----------
    detached = detach()
    assert not has_session()
    detached.h1('Дописан через объектный API')
    detached.page_numbers()
    detached.save('session_3.docx')

    print('Saved: session_1.docx, session_2.docx, session_3.docx')


if __name__ == '__main__':
    main()