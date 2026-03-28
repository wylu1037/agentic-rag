from io import BytesIO
from pathlib import Path
from typing import Any


class DoclingParser:
    def __init__(self, converter: Any | None = None) -> None:
        self._converter = converter

    def parse(self, content: bytes | str, filename: str) -> str:
        suffix = Path(filename).suffix.lower()

        if isinstance(content, str):
            return self._parse_text_content(content, filename, suffix)

        return self._parse_binary_content(content, filename, suffix)

    def _parse_text_content(self, content: str, filename: str, suffix: str) -> str:
        if suffix in {".md", ".markdown", ".qmd", ".rmd"}:
            return self._convert_string(content, filename, "MD")
        if suffix in {".html", ".htm"}:
            return self._convert_string(content, filename, "HTML")
        return content

    def _parse_binary_content(self, content: bytes, filename: str, suffix: str) -> str:
        if suffix in {".txt", ".text"}:
            return content.decode("utf-8")

        if suffix in {".md", ".markdown", ".qmd", ".rmd"}:
            return self._convert_string(content.decode("utf-8"), filename, "MD")

        if suffix in {".html", ".htm"}:
            return self._convert_string(content.decode("utf-8"), filename, "HTML")

        converter = self._get_converter()
        document_stream = self._build_document_stream(filename, content)
        result = converter.convert(document_stream)
        return result.document.export_to_markdown()

    def _convert_string(self, content: str, filename: str, input_format_name: str) -> str:
        converter = self._get_converter()
        input_format = self._get_input_format(input_format_name)
        result = converter.convert_string(content, format=input_format, name=filename)
        return result.document.export_to_markdown()

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

    @staticmethod
    def _get_input_format(name: str) -> Any:
        from docling.datamodel.base_models import InputFormat

        return getattr(InputFormat, name)

    @staticmethod
    def _build_document_stream(filename: str, content: bytes) -> Any:
        from docling.datamodel.base_models import DocumentStream

        return DocumentStream(name=filename, stream=BytesIO(content))
