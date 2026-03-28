from io import BytesIO
from pathlib import Path
from typing import Any

from app.domain.models import ParsedContent, ParsedSection


class DoclingParser:
    def __init__(self, converter: Any | None = None, docling_chunker: Any | None = None) -> None:
        self._converter = converter
        self._docling_chunker = docling_chunker

    def parse(self, content: bytes | str, filename: str) -> ParsedContent:
        suffix = Path(filename).suffix.lower()

        if isinstance(content, str):
            return self._parse_text_content(content, filename, suffix)

        return self._parse_binary_content(content, filename, suffix)

    def _parse_text_content(self, content: str, filename: str, suffix: str) -> ParsedContent:
        if suffix in {".md", ".markdown", ".qmd", ".rmd"}:
            return self._convert_string(content, filename, "MD", "markdown")
        if suffix in {".html", ".htm"}:
            return self._convert_string(content, filename, "HTML", "html")
        return ParsedContent(
            text=content,
            content_type=self._detect_content_type(filename),
            metadata={"parser": "plaintext"},
        )

    def _parse_binary_content(self, content: bytes, filename: str, suffix: str) -> ParsedContent:
        if suffix in {".txt", ".text"}:
            return ParsedContent(
                text=content.decode("utf-8"),
                content_type="text",
                metadata={"parser": "plaintext"},
            )

        if suffix in {".md", ".markdown", ".qmd", ".rmd"}:
            return self._convert_string(content.decode("utf-8"), filename, "MD", "markdown")

        if suffix in {".html", ".htm"}:
            return self._convert_string(content.decode("utf-8"), filename, "HTML", "html")

        converter = self._get_converter()
        document_stream = self._build_document_stream(filename, content)
        result = converter.convert(document_stream)
        return self._to_parsed_content(result.document, filename)

    def _convert_string(
        self,
        content: str,
        filename: str,
        input_format_name: str,
        content_type: str,
    ) -> ParsedContent:
        converter = self._get_converter()
        input_format = self._get_input_format(input_format_name)
        result = converter.convert_string(content, format=input_format, name=filename)
        return self._to_parsed_content(result.document, filename, content_type=content_type)

    def _to_parsed_content(
        self,
        document: Any,
        filename: str,
        content_type: str | None = None,
    ) -> ParsedContent:
        origin = self._get_attr(document, "origin")
        metadata = {
            "parser": "docling",
            "filename": filename,
        }

        mimetype = self._get_attr(origin, "mimetype")
        if mimetype:
            metadata["mime_type"] = mimetype

        detected_type = content_type or self._detect_content_type(filename)
        sections = self._build_sections(document)
        return ParsedContent(
            text=document.export_to_markdown(),
            content_type=detected_type,
            metadata=metadata,
            sections=sections,
        )

    def _build_sections(self, document: Any) -> list[ParsedSection]:
        chunker = self._get_docling_chunker()
        sections: list[ParsedSection] = []

        for chunk in chunker.chunk(dl_doc=document):
            text = getattr(chunk, "text", "").strip()
            if not text:
                continue

            meta = getattr(chunk, "meta", None)
            headings = self._coerce_list(self._get_attr(meta, "headings"))
            page_numbers = self._extract_page_numbers(self._get_attr(meta, "doc_items"))
            origin = self._get_attr(meta, "origin")

            section_metadata: dict[str, Any] = {}
            if headings:
                section_metadata["heading_path"] = " > ".join(headings)
            if page_numbers:
                section_metadata["page_numbers"] = page_numbers

            origin_mimetype = self._get_attr(origin, "mimetype")
            if origin_mimetype:
                section_metadata["mime_type"] = origin_mimetype

            sections.append(ParsedSection(text=text, metadata=section_metadata))

        if sections:
            return sections

        return [ParsedSection(text=document.export_to_markdown())]

    def _get_converter(self) -> Any:
        if self._converter is not None:
            return self._converter

        try:
            from docling.document_converter import DocumentConverter
        except ImportError as exc:  # pragma: no cover - exercised by runtime setup
            raise RuntimeError(
                "Docling is required for document parsing. Install backend dependencies first."
            ) from exc

        self._converter = DocumentConverter()
        return self._converter

    def _get_docling_chunker(self) -> Any:
        if self._docling_chunker is not None:
            return self._docling_chunker

        try:
            from docling_core.transforms.chunker import HierarchicalChunker
        except ImportError as exc:  # pragma: no cover - exercised by runtime setup
            raise RuntimeError(
                "Docling chunking support is required. Install backend dependencies first."
            ) from exc

        self._docling_chunker = HierarchicalChunker()
        return self._docling_chunker

    @staticmethod
    def _get_input_format(name: str) -> Any:
        from docling.datamodel.base_models import InputFormat

        return getattr(InputFormat, name)

    @staticmethod
    def _build_document_stream(filename: str, content: bytes) -> Any:
        from docling.datamodel.base_models import DocumentStream

        return DocumentStream(name=filename, stream=BytesIO(content))

    @staticmethod
    def _get_attr(value: Any, name: str) -> Any:
        if value is None:
            return None
        if hasattr(value, name):
            return getattr(value, name)
        if isinstance(value, dict):
            return value.get(name)
        return None

    def _extract_page_numbers(self, doc_items: Any) -> list[int]:
        page_numbers: set[int] = set()
        for doc_item in self._coerce_list(doc_items):
            for prov in self._coerce_list(self._get_attr(doc_item, "prov")):
                page_no = self._get_attr(prov, "page_no")
                if isinstance(page_no, int):
                    page_numbers.add(page_no)
        return sorted(page_numbers)

    @staticmethod
    def _coerce_list(value: Any) -> list[Any]:
        if value is None:
            return []
        if isinstance(value, list):
            return value
        if isinstance(value, tuple):
            return list(value)
        return [value]

    @staticmethod
    def _detect_content_type(filename: str) -> str:
        lower = filename.lower()
        if lower.endswith((".md", ".markdown", ".qmd", ".rmd")):
            return "markdown"
        if lower.endswith((".html", ".htm")):
            return "html"
        if lower.endswith(".csv"):
            return "csv"
        if lower.endswith(".pdf"):
            return "pdf"
        if lower.endswith(".docx"):
            return "docx"
        if lower.endswith(".pptx"):
            return "pptx"
        if lower.endswith(".xlsx"):
            return "xlsx"
        if lower.endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".webp")):
            return "image"
        return "text"
