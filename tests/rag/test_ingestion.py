import pytest

from app.rag.ingestion.dedup import Deduplicator
from app.rag.ingestion.parser import (
    DocumentParser,
    UnsupportedDocumentTypeError,
    compute_content_hash,
)
from app.rag.ingestion.repository import RagRepository


def test_compute_content_hash_is_deterministic():
    assert compute_content_hash("hello") == compute_content_hash("hello")
    assert compute_content_hash("hello") != compute_content_hash("world")


def test_parse_text_derives_a_stable_id_from_content_hash():
    parser = DocumentParser()
    doc = parser.parse_text("hello world", source="test", title="Test")
    assert doc.id == f"doc-{doc.content_hash[:16]}"
    assert doc.content == "hello world"


def test_parse_file_rejects_unsupported_suffix(tmp_path):
    bad_file = tmp_path / "notes.docx"
    bad_file.write_text("irrelevant")
    with pytest.raises(UnsupportedDocumentTypeError):
        DocumentParser().parse_file(bad_file)


def test_parse_file_allows_title_and_source_override(tmp_path):
    file_path = tmp_path / "tmp12345.txt"
    file_path.write_text("some content")
    doc = DocumentParser().parse_file(file_path, source="original.txt", title="Original")
    assert doc.source == "original.txt"
    assert doc.title == "Original"


def test_repository_round_trips_documents_and_chunks():
    from app.models.rag import Chunk

    repo = RagRepository("sqlite:///:memory:")
    doc = DocumentParser().parse_text("hello world", source="s", title="T")
    repo.save_document(doc)
    repo.save_chunks(
        [Chunk(id="c1", document_id=doc.id, content="hello", chunk_index=0, strategy="recursive")]
    )

    assert repo.document_count() == 1
    assert repo.chunk_count() == 1
    assert repo.find_document_by_hash(doc.content_hash).id == doc.id
    assert repo.chunks_for_document(doc.id)[0].id == "c1"
    assert repo.get_chunk("c1").content == "hello"
    assert repo.get_chunk("does-not-exist") is None


def test_deduplicator_detects_repeat_content():
    repo = RagRepository("sqlite:///:memory:")
    dedup = Deduplicator(repo)
    doc = DocumentParser().parse_text("same content", source="s", title="T")

    first = dedup.check(doc)
    assert first.is_duplicate is False

    repo.save_document(doc)
    second = dedup.check(doc)
    assert second.is_duplicate is True
    assert second.existing_document.id == doc.id
