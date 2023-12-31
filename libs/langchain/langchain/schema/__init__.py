"""**Schemas** are the LangChain Base Classes and Interfaces."""
from langchain.libs.core.langchain_core.agents import AgentAction, AgentFinish
from langchain.libs.core.langchain_core.caches import BaseCache
from langchain.libs.core.langchain_core.chat_history import BaseChatMessageHistory
from langchain.libs.core.langchain_core.documents import BaseDocumentTransformer, Document
from langchain.libs.core.langchain_core.exceptions import LangChainException, OutputParserException
from langchain.libs.core.langchain_core.memory import BaseMemory
from langchain.libs.core.langchain_core.messages import (
    AIMessage,
    BaseMessage,
    ChatMessage,
    FunctionMessage,
    HumanMessage,
    SystemMessage,
    _message_from_dict,
    get_buffer_string,
    messages_from_dict,
    messages_to_dict,
)
from langchain.libs.core.langchain_core.messages.base import message_to_dict
from langchain.libs.core.langchain_core.output_parsers import (
    BaseLLMOutputParser,
    BaseOutputParser,
    StrOutputParser,
)
from langchain.libs.core.langchain_core.outputs import (
    ChatGeneration,
    ChatResult,
    Generation,
    LLMResult,
    RunInfo,
)
from langchain.libs.core.langchain_core.prompt_values import PromptValue
from langchain.libs.core.langchain_core.prompts import BasePromptTemplate, format_document
from langchain.libs.core.langchain_core.retrievers import BaseRetriever
from langchain.libs.core.langchain_core.stores import BaseStore

RUN_KEY = "__run"

# Backwards compatibility.
Memory = BaseMemory
_message_to_dict = message_to_dict

__all__ = [
    "BaseCache",
    "BaseMemory",
    "BaseStore",
    "AgentFinish",
    "AgentAction",
    "Document",
    "BaseChatMessageHistory",
    "BaseDocumentTransformer",
    "BaseMessage",
    "ChatMessage",
    "FunctionMessage",
    "HumanMessage",
    "AIMessage",
    "SystemMessage",
    "messages_from_dict",
    "messages_to_dict",
    "message_to_dict",
    "_message_to_dict",
    "_message_from_dict",
    "get_buffer_string",
    "RunInfo",
    "LLMResult",
    "ChatResult",
    "ChatGeneration",
    "Generation",
    "PromptValue",
    "LangChainException",
    "BaseRetriever",
    "RUN_KEY",
    "Memory",
    "OutputParserException",
    "StrOutputParser",
    "BaseOutputParser",
    "BaseLLMOutputParser",
    "BasePromptTemplate",
    "format_document",
]
