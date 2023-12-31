# Backwards compatibility.
from langchain.libs.core.langchain_core.language_models import BaseLanguageModel
from langchain.libs.core.langchain_core.language_models.llms import (
    LLM,
    BaseLLM,
)

__all__ = [
    "BaseLanguageModel",
    "BaseLLM",
    "LLM",
]
