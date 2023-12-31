# ruff: noqa: E402
"""Main entrypoint into package."""
import warnings
from importlib import metadata
from typing import Any, Optional

from langchain_core._api.deprecation import surface_langchain_deprecation_warnings


try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    # Case where package metadata is not available.
    __version__ = ""
del metadata  # optional, avoids polluting the results of dir(__package__)


def _is_interactive_env() -> bool:
    """Determine if running within IPython or Jupyter."""
    import sys

    return hasattr(sys, "ps2")


def _warn_on_import(name: str, replacement: Optional[str] = None) -> None:
    """Warn on import of deprecated module."""
    if _is_interactive_env():
        # No warnings for interactive environments.
        # This is done to avoid polluting the output of interactive environments
        # where users rely on auto-complete and may trigger this warning
        # even if they are not using any deprecated modules
        return

    if replacement:
        warnings.warn(
            f"Importing {name} from langchain root module is no longer supported. "
            f"Please use {replacement} instead."
        )
    else:
        warnings.warn(
            f"Importing {name} from langchain root module is no longer supported."
        )


# Surfaces Deprecation and Pending Deprecation warnings from langchain.
surface_langchain_deprecation_warnings()


def __getattr__(name: str) -> Any:
    if name == "MRKLChain":
        from langchain.agents import MRKLChain

        _warn_on_import(name, replacement="langchain.agents.MRKLChain")

        return MRKLChain
    elif name == "ReActChain":
        from langchain.agents import ReActChain

        _warn_on_import(name, replacement="langchain.agents.ReActChain")

        return ReActChain
    elif name == "SelfAskWithSearchChain":
        from langchain.agents import SelfAskWithSearchChain

        _warn_on_import(name, replacement="langchain.agents.SelfAskWithSearchChain")

        return SelfAskWithSearchChain
    elif name == "ConversationChain":
        from langchain.libs.langchain.langchain.chains import ConversationChain

        _warn_on_import(name, replacement="langchain.chains.ConversationChain")

        return ConversationChain
    elif name == "LLMBashChain":
        raise ImportError(
            "This module has been moved to langchain-experimental. "
            "For more details: "
            "https://github.com/langchain-ai/langchain/discussions/11352."
            "To access this code, install it with `pip install langchain-experimental`."
            "`from langchain_experimental.llm_bash.base "
            "import LLMBashChain`"
        )

    elif name == "LLMChain":
        from langchain.libs.langchain.langchain.chains import LLMChain

        _warn_on_import(name, replacement="langchain.chains.LLMChain")

        return LLMChain
    elif name == "LLMCheckerChain":
        from langchain.libs.langchain.langchain.chains import LLMCheckerChain

        _warn_on_import(name, replacement="langchain.chains.LLMCheckerChain")

        return LLMCheckerChain
    elif name == "LLMMathChain":
        from langchain.libs.langchain.langchain.chains import LLMMathChain

        _warn_on_import(name, replacement="langchain.chains.LLMMathChain")

        return LLMMathChain
    elif name == "QAWithSourcesChain":
        from langchain.libs.langchain.langchain.chains import QAWithSourcesChain

        _warn_on_import(name, replacement="langchain.chains.QAWithSourcesChain")

        return QAWithSourcesChain
    elif name == "VectorDBQA":
        from langchain.libs.langchain.langchain.chains import VectorDBQA

        _warn_on_import(name, replacement="langchain.chains.VectorDBQA")

        return VectorDBQA
    elif name == "VectorDBQAWithSourcesChain":
        from langchain.libs.langchain.langchain.chains import VectorDBQAWithSourcesChain

        _warn_on_import(name, replacement="langchain.chains.VectorDBQAWithSourcesChain")

        return VectorDBQAWithSourcesChain
    elif name == "InMemoryDocstore":
        from langchain.docstore import InMemoryDocstore

        _warn_on_import(name, replacement="langchain.docstore.InMemoryDocstore")

        return InMemoryDocstore
    elif name == "Wikipedia":
        from langchain.docstore import Wikipedia

        _warn_on_import(name, replacement="langchain.docstore.Wikipedia")

        return Wikipedia
    elif name == "Anthropic":
        from langchain.libs.langchain.langchain.llms import Anthropic

        _warn_on_import(name, replacement="langchain.llms.Anthropic")

        return Anthropic
    elif name == "Banana":
        from langchain.libs.langchain.langchain.llms import Banana

        _warn_on_import(name, replacement="langchain.llms.Banana")

        return Banana
    elif name == "CerebriumAI":
        from langchain.libs.langchain.langchain.llms import CerebriumAI

        _warn_on_import(name, replacement="langchain.llms.CerebriumAI")

        return CerebriumAI
    elif name == "Cohere":
        from langchain.libs.langchain.langchain.llms import Cohere

        _warn_on_import(name, replacement="langchain.llms.Cohere")

        return Cohere
    elif name == "ForefrontAI":
        from langchain.libs.langchain.langchain.llms import ForefrontAI

        _warn_on_import(name, replacement="langchain.llms.ForefrontAI")

        return ForefrontAI
    elif name == "GooseAI":
        from langchain.libs.langchain.langchain.llms import GooseAI

        _warn_on_import(name, replacement="langchain.llms.GooseAI")

        return GooseAI
    elif name == "HuggingFaceHub":
        from langchain.libs.langchain.langchain.llms import HuggingFaceHub

        _warn_on_import(name, replacement="langchain.llms.HuggingFaceHub")

        return HuggingFaceHub
    elif name == "HuggingFaceTextGenInference":
        from langchain.libs.langchain.langchain.llms import HuggingFaceTextGenInference

        _warn_on_import(name, replacement="langchain.llms.HuggingFaceTextGenInference")

        return HuggingFaceTextGenInference
    elif name == "LlamaCpp":
        from langchain.libs.langchain.langchain.llms import LlamaCpp

        _warn_on_import(name, replacement="langchain.llms.LlamaCpp")

        return LlamaCpp
    elif name == "Modal":
        from langchain.libs.langchain.langchain.llms import Modal

        _warn_on_import(name, replacement="langchain.llms.Modal")

        return Modal
    elif name == "OpenAI":
        from langchain.libs.langchain.langchain.llms import OpenAI

        _warn_on_import(name, replacement="langchain.llms.OpenAI")

        return OpenAI
    elif name == "Petals":
        from langchain.libs.langchain.langchain.llms import Petals

        _warn_on_import(name, replacement="langchain.llms.Petals")

        return Petals
    elif name == "PipelineAI":
        from langchain.libs.langchain.langchain.llms import PipelineAI

        _warn_on_import(name, replacement="langchain.llms.PipelineAI")

        return PipelineAI
    elif name == "SagemakerEndpoint":
        from langchain.libs.langchain.langchain.llms import SagemakerEndpoint

        _warn_on_import(name, replacement="langchain.llms.SagemakerEndpoint")

        return SagemakerEndpoint
    elif name == "StochasticAI":
        from langchain.libs.langchain.langchain.llms import StochasticAI

        _warn_on_import(name, replacement="langchain.llms.StochasticAI")

        return StochasticAI
    elif name == "Writer":
        from langchain.libs.langchain.langchain.llms import Writer

        _warn_on_import(name, replacement="langchain.llms.Writer")

        return Writer
    elif name == "HuggingFacePipeline":
        from langchain.libs.langchain.langchain.llms.huggingface_pipeline import HuggingFacePipeline

        _warn_on_import(
            name, replacement="langchain.llms.huggingface_pipeline.HuggingFacePipeline"
        )

        return HuggingFacePipeline
    elif name == "FewShotPromptTemplate":
        from langchain.libs.core.langchain_core.prompts import FewShotPromptTemplate

        _warn_on_import(name, replacement="langchain.prompts.FewShotPromptTemplate")

        return FewShotPromptTemplate
    elif name == "Prompt":
        from langchain.prompts import Prompt

        _warn_on_import(name, replacement="langchain.prompts.Prompt")

        return Prompt
    elif name == "PromptTemplate":
        from langchain.libs.core.langchain_core.prompts import PromptTemplate

        _warn_on_import(name, replacement="langchain.prompts.PromptTemplate")

        return PromptTemplate
    elif name == "BasePromptTemplate":
        from langchain.libs.core.langchain_core.prompts import BasePromptTemplate

        _warn_on_import(
            name, replacement="langchain.schema.prompt_template.BasePromptTemplate"
        )

        return BasePromptTemplate
    elif name == "ArxivAPIWrapper":
        from langchain.libs.langchain.langchain.utilities import ArxivAPIWrapper

        _warn_on_import(name, replacement="langchain.utilities.ArxivAPIWrapper")

        return ArxivAPIWrapper
    elif name == "GoldenQueryAPIWrapper":
        from langchain.libs.langchain.langchain.utilities import GoldenQueryAPIWrapper

        _warn_on_import(name, replacement="langchain.utilities.GoldenQueryAPIWrapper")

        return GoldenQueryAPIWrapper
    elif name == "GoogleSearchAPIWrapper":
        from langchain.libs.langchain.langchain.utilities import GoogleSearchAPIWrapper

        _warn_on_import(name, replacement="langchain.utilities.GoogleSearchAPIWrapper")

        return GoogleSearchAPIWrapper
    elif name == "GoogleSerperAPIWrapper":
        from langchain.libs.langchain.langchain.utilities import GoogleSerperAPIWrapper

        _warn_on_import(name, replacement="langchain.utilities.GoogleSerperAPIWrapper")

        return GoogleSerperAPIWrapper
    elif name == "PowerBIDataset":
        from langchain.libs.langchain.langchain.utilities import PowerBIDataset

        _warn_on_import(name, replacement="langchain.utilities.PowerBIDataset")

        return PowerBIDataset
    elif name == "SearxSearchWrapper":
        from langchain.libs.langchain.langchain.utilities import SearxSearchWrapper

        _warn_on_import(name, replacement="langchain.utilities.SearxSearchWrapper")

        return SearxSearchWrapper
    elif name == "WikipediaAPIWrapper":
        from langchain.libs.langchain.langchain.utilities import WikipediaAPIWrapper

        _warn_on_import(name, replacement="langchain.utilities.WikipediaAPIWrapper")

        return WikipediaAPIWrapper
    elif name == "WolframAlphaAPIWrapper":
        from langchain.libs.langchain.langchain.utilities import WolframAlphaAPIWrapper

        _warn_on_import(name, replacement="langchain.utilities.WolframAlphaAPIWrapper")

        return WolframAlphaAPIWrapper
    elif name == "SQLDatabase":
        from langchain.libs.langchain.langchain.utilities import SQLDatabase

        _warn_on_import(name, replacement="langchain.utilities.SQLDatabase")

        return SQLDatabase
    elif name == "FAISS":
        from langchain.libs.langchain.langchain.vectorstores import FAISS

        _warn_on_import(name, replacement="langchain.vectorstores.FAISS")

        return FAISS
    elif name == "ElasticVectorSearch":
        from langchain.libs.langchain.langchain.vectorstores import ElasticVectorSearch

        _warn_on_import(name, replacement="langchain.vectorstores.ElasticVectorSearch")

        return ElasticVectorSearch
    # For backwards compatibility
    elif name == "SerpAPIChain" or name == "SerpAPIWrapper":
        from langchain.libs.langchain.langchain.utilities import SerpAPIWrapper

        _warn_on_import(name, replacement="langchain.utilities.SerpAPIWrapper")

        return SerpAPIWrapper
    elif name == "verbose":
        from langchain.libs.langchain.langchain.globals import _verbose

        _warn_on_import(
            name,
            replacement=(
                "langchain.globals.set_verbose() / langchain.globals.get_verbose()"
            ),
        )

        return _verbose
    elif name == "debug":
        from langchain.libs.langchain.langchain.globals import _debug

        _warn_on_import(
            name,
            replacement=(
                "langchain.globals.set_debug() / langchain.globals.get_debug()"
            ),
        )

        return _debug
    elif name == "llm_cache":
        from langchain.libs.langchain.langchain.globals import _llm_cache

        _warn_on_import(
            name,
            replacement=(
                "langchain.globals.set_llm_cache() / langchain.globals.get_llm_cache()"
            ),
        )

        return _llm_cache
    else:
        raise AttributeError(f"Could not find: {name}")


__all__ = [
    "LLMChain",
    "LLMCheckerChain",
    "LLMMathChain",
    "ArxivAPIWrapper",
    "GoldenQueryAPIWrapper",
    "SelfAskWithSearchChain",
    "SerpAPIWrapper",
    "SerpAPIChain",
    "SearxSearchWrapper",
    "GoogleSearchAPIWrapper",
    "GoogleSerperAPIWrapper",
    "WolframAlphaAPIWrapper",
    "WikipediaAPIWrapper",
    "Anthropic",
    "Banana",
    "CerebriumAI",
    "Cohere",
    "ForefrontAI",
    "GooseAI",
    "Modal",
    "OpenAI",
    "Petals",
    "PipelineAI",
    "StochasticAI",
    "Writer",
    "BasePromptTemplate",
    "Prompt",
    "FewShotPromptTemplate",
    "PromptTemplate",
    "ReActChain",
    "Wikipedia",
    "HuggingFaceHub",
    "SagemakerEndpoint",
    "HuggingFacePipeline",
    "SQLDatabase",
    "PowerBIDataset",
    "FAISS",
    "MRKLChain",
    "VectorDBQA",
    "ElasticVectorSearch",
    "InMemoryDocstore",
    "ConversationChain",
    "VectorDBQAWithSourcesChain",
    "QAWithSourcesChain",
    "LlamaCpp",
    "HuggingFaceTextGenInference",
]
