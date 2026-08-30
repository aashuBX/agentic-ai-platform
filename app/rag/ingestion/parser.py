"""Document parsing: turns a file or raw text into a `Document`, with its content hash attached."""

import hashlib
from pathlib import Path

from app.models.rag import Document


def compute_content_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


class UnsupportedDocumentTypeError(ValueError):
    pass


class DocumentParser:
    """Supports `.txt`/`.md` directly. `.pdf` uses `pypdf` (a base dependency — see pyproject.toml),
    imported lazily so parsing text/markdown never touches it and a stripped-down environment
    missing it still works for the two common cases.
    """

    SUPPORTED_SUFFIXES = (".txt", ".md", ".pdf")

    def parse_file(
        self,
        file_path: str | Path,
        *,
        source: str | None = None,
        title: str | None = None,
        extra_metadata: dict | None = None,
    ) -> Document:
        """`source`/`title` default to the file path/stem — override them when `file_path` is a
        throwaway location (e.g. a temp file backing an API upload) and shouldn't leak into the
        document's identity."""

        path = Path(file_path)
        suffix = path.suffix.lower()
        if suffix not in self.SUPPORTED_SUFFIXES:
            raise UnsupportedDocumentTypeError(
                f"Unsupported document type {suffix!r}. Supported: {self.SUPPORTED_SUFFIXES}"
            )
        content = self._read_pdf(path) if suffix == ".pdf" else path.read_text(encoding="utf-8")
        return self.parse_text(
            content,
            source=source or str(path),
            title=title or path.stem,
            extra_metadata=extra_metadata,
        )

    def parse_text(
        self, content: str, *, source: str, title: str, extra_metadata: dict | None = None
    ) -> Document:
        content_hash = compute_content_hash(content)
        return Document(
            id=f"doc-{content_hash[:16]}",
            source=source,
            title=title,
            content=content,
            content_hash=content_hash,
            metadata=extra_metadata or {},
        )

    @staticmethod
    def _read_pdf(path: Path) -> str:
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise UnsupportedDocumentTypeError(
                'Reading .pdf files requires "pypdf" (pip install -e . reinstalls base dependencies)'
            ) from exc
        reader = PdfReader(str(path))
        return "\n\n".join(page.extract_text() or "" for page in reader.pages)
