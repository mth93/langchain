from __future__ import annotations

from typing import Iterator, List

import requests
from libs.core.langchain_core.documents import Document

from langchain_community.document_loaders.base import BaseLoader


class ToMarkdownLoader(BaseLoader):
    """Load `HTML` using `2markdown API`."""

    def __init__(self, url: str, api_key: str):
        """Initialize with url and api key."""
        self.url = url
        self.api_key = api_key

    def lazy_load(
        self,
    ) -> Iterator[Document]:
        """Lazily load the file."""
        response = requests.post(
            "https://2markdown.com/api/2md",
            headers={"X-Api-Key": self.api_key},
            json={"url": self.url},
        )
        text = response.json()["article"]
        metadata = {"source": self.url}
        yield Document(page_content=text, metadata=metadata)

    def load(self) -> List[Document]:
        """Load file."""
        return list(self.lazy_load())
