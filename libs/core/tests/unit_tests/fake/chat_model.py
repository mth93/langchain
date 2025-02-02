"""Fake ChatModel for testing purposes."""
import asyncio
import time
from typing import Any, AsyncIterator, Dict, Iterator, List, Optional, Union

from langchain.libs.core.langchain_core.callbacks.manager import (
    AsyncCallbackManagerForLLMRun,
    CallbackManagerForLLMRun,
)
from langchain.libs.core.langchain_core.language_models.chat_models import BaseChatModel, SimpleChatModel
from langchain.libs.core.langchain_core.messages import AIMessageChunk, BaseMessage
from langchain.libs.core.langchain_core.outputs import ChatGeneration, ChatGenerationChunk, ChatResult


class FakeMessagesListChatModel(BaseChatModel):
    """Fake ChatModel for testing purposes."""

    responses: List[BaseMessage]
    sleep: Optional[float] = None
    i: int = 0

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        response = self.responses[self.i]
        if self.i < len(self.responses) - 1:
            self.i += 1
        else:
            self.i = 0
        generation = ChatGeneration(message=response)
        return ChatResult(generations=[generation])

    @property
    def _llm_type(self) -> str:
        return "fake-messages-list-chat-model"


class FakeListChatModel(SimpleChatModel):
    """Fake ChatModel for testing purposes."""

    responses: List
    sleep: Optional[float] = None
    i: int = 0
    error_on_chunk_number: Optional[int] = None

    @property
    def _llm_type(self) -> str:
        return "fake-list-chat-model"

    def _call(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """First try to lookup in queries, else return 'foo' or 'bar'."""
        response = self.responses[self.i]
        if self.i < len(self.responses) - 1:
            self.i += 1
        else:
            self.i = 0
        return response

    def _stream(
        self,
        messages: List[BaseMessage],
        stop: Union[List[str], None] = None,
        run_manager: Union[CallbackManagerForLLMRun, None] = None,
        **kwargs: Any,
    ) -> Iterator[ChatGenerationChunk]:
        response = self.responses[self.i]
        if self.i < len(self.responses) - 1:
            self.i += 1
        else:
            self.i = 0
        for i_c, c in enumerate(response):
            if self.sleep is not None:
                time.sleep(self.sleep)
            if (
                self.error_on_chunk_number is not None
                and i_c == self.error_on_chunk_number
            ):
                raise Exception("Fake error")

            yield ChatGenerationChunk(message=AIMessageChunk(content=c))

    async def _astream(
        self,
        messages: List[BaseMessage],
        stop: Union[List[str], None] = None,
        run_manager: Union[AsyncCallbackManagerForLLMRun, None] = None,
        **kwargs: Any,
    ) -> AsyncIterator[ChatGenerationChunk]:
        response = self.responses[self.i]
        if self.i < len(self.responses) - 1:
            self.i += 1
        else:
            self.i = 0
        for i_c, c in enumerate(response):
            if self.sleep is not None:
                await asyncio.sleep(self.sleep)
            if (
                self.error_on_chunk_number is not None
                and i_c == self.error_on_chunk_number
            ):
                raise Exception("Fake error")
            yield ChatGenerationChunk(message=AIMessageChunk(content=c))

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        return {"responses": self.responses}
