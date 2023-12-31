"""Memory modules for conversation prompts."""

from langchain.libs.langchain.langchain.memory.buffer import (
    ConversationBufferMemory,
    ConversationStringBufferMemory,
)
from langchain.libs.langchain.langchain.memory.buffer_window import ConversationBufferWindowMemory
from langchain.libs.langchain.langchain.memory.combined import CombinedMemory
from langchain.libs.langchain.langchain.memory.entity import ConversationEntityMemory
from langchain.libs.langchain.langchain.memory.kg import ConversationKGMemory
from langchain.libs.langchain.langchain.memory.summary import ConversationSummaryMemory
from langchain.libs.langchain.langchain.memory.summary_buffer import ConversationSummaryBufferMemory

# This is only for backwards compatibility.

__all__ = [
    "ConversationSummaryBufferMemory",
    "ConversationSummaryMemory",
    "ConversationKGMemory",
    "ConversationBufferWindowMemory",
    "ConversationEntityMemory",
    "ConversationBufferMemory",
    "CombinedMemory",
    "ConversationStringBufferMemory",
]
