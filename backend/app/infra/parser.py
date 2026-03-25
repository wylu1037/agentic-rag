class MarkdownParser:
    def parse(self, content: bytes | str, filename: str) -> str:
        if isinstance(content, bytes):
            content = content.decode("utf-8")
        return content
