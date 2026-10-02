"""Single point of import for the real python-docx Document class.

The name `Document` is exported from `docx.api` as a factory function,
not as a class. Using it in type annotations fails: mypy reports
"Function 'Document' is not valid as a type". The real class lives in
`docx.document`; the factory returns instances of it.

Re-exporting under the name DocxDocument gives every module in the
package a single, unambiguous handle for the class, without the
function-versus-class confusion.
"""
from docx.document import Document as DocxDocument


__all__ = ['DocxDocument']