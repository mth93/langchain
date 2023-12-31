# Backwards compatibility.
from libs.core.langchain_core.language_models import BaseLanguageModel
from libs.core.langchain_core.language_models.llms import (
    LLM,
    BaseLLM,
)

__all__ = [
    "BaseLanguageModel",
    "BaseLLM",
    "LLM",
]
