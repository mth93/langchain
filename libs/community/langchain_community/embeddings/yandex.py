"""Wrapper around YandexGPT embedding models."""
from __future__ import annotations

import logging
from typing import Any, Callable, Dict, List

from langchain.libs.core.langchain_core.embeddings import Embeddings
from langchain.libs.core.langchain_core.pydantic_v1 import BaseModel, root_validator
from langchain.libs.core.langchain_core.utils import get_from_dict_or_env
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

logger = logging.getLogger(__name__)


class YandexGPTEmbeddings(BaseModel, Embeddings):
    """YandexGPT Embeddings models.

    To use, you should have the ``yandexcloud`` python package installed.

    There are two authentication options for the service account
    with the ``ai.languageModels.user`` role:
        - You can specify the token in a constructor parameter `iam_token`
        or in an environment variable `YC_IAM_TOKEN`.
        - You can specify the key in a constructor parameter `api_key`
        or in an environment variable `YC_API_KEY`.

    To use the default model specify the folder ID in a parameter `folder_id`
    or in an environment variable `YC_FOLDER_ID`.
    Or specify the model URI in a constructor parameter `model_uri`

    Example:
        .. code-block:: python

            from langchain_community.embeddings.yandex import YandexGPTEmbeddings
            embeddings = YandexGPTEmbeddings(iam_token="t1.9eu...", model_uri="emb://<folder-id>/text-search-query/latest")
    """

    iam_token: str = ""
    """Yandex Cloud IAM token for service account
    with the `ai.languageModels.user` role"""
    api_key: str = ""
    """Yandex Cloud Api Key for service account
    with the `ai.languageModels.user` role"""
    model_uri: str = ""
    """Model uri to use."""
    folder_id: str = ""
    """Yandex Cloud folder ID"""
    model_uri: str = ""
    """Model uri to use."""
    model_name: str = "text-search-query"
    """Model name to use."""
    model_version: str = "latest"
    """Model version to use."""
    url: str = "llm.api.cloud.yandex.net:443"
    """The url of the API."""
    max_retries: int = 6
    """Maximum number of retries to make when generating."""

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that iam token exists in environment."""

        iam_token = get_from_dict_or_env(values, "iam_token", "YC_IAM_TOKEN", "")
        values["iam_token"] = iam_token
        api_key = get_from_dict_or_env(values, "api_key", "YC_API_KEY", "")
        values["api_key"] = api_key
        folder_id = get_from_dict_or_env(values, "folder_id", "YC_FOLDER_ID", "")
        values["folder_id"] = folder_id
        if api_key == "" and iam_token == "":
            raise ValueError("Either 'YC_API_KEY' or 'YC_IAM_TOKEN' must be provided.")
        if values["iam_token"]:
            values["_grpc_metadata"] = [
                ("authorization", f"Bearer {values['iam_token']}")
            ]
            if values["folder_id"]:
                values["_grpc_metadata"].append(("x-folder-id", values["folder_id"]))
        else:
            values["_grpc_metadata"] = (
                ("authorization", f"Api-Key {values['api_key']}"),
            )
        if values["model_uri"] == "" and values["folder_id"] == "":
            raise ValueError("Either 'model_uri' or 'folder_id' must be provided.")
        if not values["model_uri"]:
            values[
                "model_uri"
            ] = f"emb://{values['folder_id']}/{values['model_name']}/{values['model_version']}"
        return values

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed documents using a YandexGPT embeddings models.

        Args:
            texts: The list of texts to embed.

        Returns:
            List of embeddings, one for each text.
        """

        return _embed_with_retry(self, texts=texts)

    def embed_query(self, text: str) -> List[float]:
        """Embed a query using a YandexGPT embeddings models.

        Args:
            text: The text to embed.

        Returns:
            Embeddings for the text.
        """
        return _embed_with_retry(self, texts=[text])[0]


def _create_retry_decorator(llm: YandexGPTEmbeddings) -> Callable[[Any], Any]:
    from grpc import RpcError

    min_seconds = 1
    max_seconds = 60
    return retry(
        reraise=True,
        stop=stop_after_attempt(llm.max_retries),
        wait=wait_exponential(multiplier=1, min=min_seconds, max=max_seconds),
        retry=(retry_if_exception_type((RpcError))),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )


def _embed_with_retry(llm: YandexGPTEmbeddings, **kwargs: Any) -> Any:
    """Use tenacity to retry the embedding call."""
    retry_decorator = _create_retry_decorator(llm)

    @retry_decorator
    def _completion_with_retry(**_kwargs: Any) -> Any:
        return _make_request(llm, **_kwargs)

    return _completion_with_retry(**kwargs)


def _make_request(self: YandexGPTEmbeddings, texts: List[str]):
    try:
        import grpc
        from yandex.cloud.ai.foundation_models.v1.foundation_models_service_pb2 import (  # noqa: E501
            TextEmbeddingRequest,
        )
        from yandex.cloud.ai.foundation_models.v1.foundation_models_service_pb2_grpc import (  # noqa: E501
            EmbeddingsServiceStub,
        )
    except ImportError as e:
        raise ImportError(
            "Please install YandexCloud SDK" " with `pip install yandexcloud`."
        ) from e
    result = []
    channel_credentials = grpc.ssl_channel_credentials()
    channel = grpc.secure_channel(self.url, channel_credentials)

    for text in texts:
        request = TextEmbeddingRequest(model_uri=self.model_uri, text=text)
        stub = EmbeddingsServiceStub(channel)
        res = stub.TextEmbedding(request, metadata=self._grpc_metadata)
        result.append(res.embedding)

    return result
