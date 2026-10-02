"""Tests for BookmarkMixin — id allocation and name preparation."""
import pytest

from docx_report_gen.styles import BOOKMARK_PREFIX


# ---------- _prepare_bookmark ----------

def test_prepare_bookmark_none_returns_none_pair(report):
    name, bid = report._prepare_bookmark(None)
    assert name is None
    assert bid is None


def test_prepare_bookmark_returns_prefixed_name_and_id(report):
    name, bid = report._prepare_bookmark('results', kind='table')
    assert name == f'{BOOKMARK_PREFIX}results'
    assert bid == 1


def test_prepare_bookmark_ids_increment(report):
    _, id1 = report._prepare_bookmark('a')
    _, id2 = report._prepare_bookmark('b')
    _, id3 = report._prepare_bookmark('c')
    assert (id1, id2, id3) == (1, 2, 3)


def test_prepare_bookmark_rejects_empty(report):
    with pytest.raises(ValueError, match='non-empty'):
        report._prepare_bookmark('', kind='table')


def test_prepare_bookmark_rejects_whitespace_only(report):
    with pytest.raises(ValueError, match='non-empty'):
        report._prepare_bookmark('   ')


def test_prepare_bookmark_rejects_internal_whitespace(report):
    with pytest.raises(ValueError, match='whitespace'):
        report._prepare_bookmark('has space')


def test_prepare_bookmark_kind_appears_in_error(report):
    with pytest.raises(ValueError, match='image'):
        report._prepare_bookmark('bad name', kind='image')


# ---------- next_bookmark_id ----------

def test_next_bookmark_id_starts_at_one(report):
    assert report.next_bookmark_id() == 1


def test_next_bookmark_id_sequential(report):
    ids = [report.next_bookmark_id() for _ in range(5)]
    assert ids == [1, 2, 3, 4, 5]


def test_ids_independent_between_reports():
    from docx_report_gen import Report
    r1 = Report()
    r2 = Report()
    assert r1.next_bookmark_id() == 1
    assert r1.next_bookmark_id() == 2
    assert r2.next_bookmark_id() == 1


# ---------- shared counter across table and image ----------

def test_table_and_image_share_bookmark_counter(report, png_image, docx_path):
    """Both mixins pull ids from the same per-Report counter."""
    report.table([['A']], caption='t', name='t1')
    report.img(png_image, caption='f', name='f1')
    report.save(str(docx_path))

    from ._helpers import bookmark_names
    names = bookmark_names(docx_path)
    assert '_Ref_t1' in names
    assert '_Ref_f1' in names
    # No collision: two distinct names present
    assert len(names) == 2