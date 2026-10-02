"""Shared fixtures for docx-report-gen tests."""
import base64

import pytest
from docx import Document

from docx_report_gen import Report
from docx_report_gen.plugins import plugins as global_plugins


# Smallest valid PNG: 1x1 transparent pixel, ~89 bytes.
# Stored as base64 so the repository has no binary blobs.
_PNG_1X1 = base64.b64decode(
    'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk'
    'YPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=='
)


@pytest.fixture(autouse=True)
def isolated_plugins():
    """Clear the global plugin registry around every test.

    The registry is process-global state. Without this fixture,
    plugins registered in one test would leak into others and
    break isolation.
    """
    global_plugins.clear()
    yield
    global_plugins.clear()


@pytest.fixture
def report():
    """Empty Report with default config."""
    return Report()


@pytest.fixture
def saved_docx(report, tmp_path):
    """A Report already saved to disk. Returns the path as Path."""
    path = tmp_path / 'report.docx'
    report.save(str(path))
    return path


@pytest.fixture
def reopen(saved_docx):
    """Callable that opens the saved docx via python-docx."""
    def _open():
        return Document(str(saved_docx))
    return _open


@pytest.fixture
def png_image(tmp_path):
    """A 1x1 transparent PNG on disk. Returns its path as str."""
    path = tmp_path / 'pixel.png'
    path.write_bytes(_PNG_1X1)
    return str(path)


@pytest.fixture
def docx_path(tmp_path):
    """A path to a .docx that does not yet exist."""
    return tmp_path / 'out.docx'