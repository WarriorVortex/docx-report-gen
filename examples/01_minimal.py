"""Minimal example: three lines to a document.

Run:
    python examples/01_minimal.py
Produces:
    minimal.docx in the current directory.
"""
from docx_report_gen import Report

r = Report()
r.h1('Hello, world')
r.p('This is the smallest possible docx-report-gen script.')
r.save('minimal.docx')