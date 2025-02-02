import json
from typing import Any, Dict, List, Optional, cast

from langchain.libs.core.langchain_core.callbacks import CallbackManagerForLLMRun
from langchain.libs.core.langchain_core.language_models.chat_models import SimpleChatModel
from langchain.libs.core.langchain_core.messages import (
    AIMessage,
    BaseMessage,
    ChatMessage,
    HumanMessage,
    SystemMessage,
)
from langchain.libs.core.langchain_core.pydantic_v1 import SecretStr, validator
from langchain.libs.core.langchain_core.utils import convert_to_secret_str, get_from_dict_or_env

from langchain_community.llms.azureml_endpoint import (
    AzureMLEndpointClient,
    ContentFormatterBase,
)


class LlamaContentFormatter(ContentFormatterBase):
    """Content formatter for `LLaMA`."""

    SUPPORTED_ROLES: List[str] = ["user", "assistant", "system"]

    @staticmethod
    def _convert_message_to_dict(message: BaseMessage) -> Dict:
        """Converts message to a dict according to role"""
        content = cast(str, message.content)
        if isinstance(message, HumanMessage):
            return {
                "role": "user",
                "content": ContentFormatterBase.escape_special_characters(content),
            }
        elif isinstance(message, AIMessage):
            return {
                "role": "assistant",
                "content": ContentFormatterBase.escape_special_characters(content),
            }
        elif isinstance(message, SystemMessage):
            return {
                "role": "system",
                "content": ContentFormatterBase.escape_special_characters(content),
            }
        elif (
            isinstance(message, ChatMessage)
            and message.role in LlamaContentFormatter.SUPPORTED_ROLES
        ):
            return {
                "role": message.role,
                "content": ContentFormatterBase.escape_special_characters(content),
            }
        else:
            supported = ",".join(
                [role for role in LlamaContentFormatter.SUPPORTED_ROLES]
            )
            raise ValueError(
                f"""Received unsupported role. 
                Supported roles for the LLaMa Foundation Model: {supported}"""
            )

    def _format_request_payload(
        self, messages: List[BaseMessage], model_kwargs: Dict
    ) -> bytes:
        chat_messages = [
            LlamaContentFormatter._convert_message_to_dict(message)
            for message in messages
        ]
        prompt = json.dumps(
            {"input_data": {"input_string": chat_messages, "parameters": model_kwargs}}
        )
        return self.format_request_payload(prompt=prompt, model_kwargs=model_kwargs)

    def format_request_payload(self, prompt: str, model_kwargs: Dict) -> bytes:
        """Formats the request according to the chosen api"""
        return str.encode(prompt)

    def format_response_payload(self, output: bytes) -> str:
        """Formats response"""
        return json.loads(output)["output"]


class AzureMLChatOnlineEndpoint(SimpleChatModel):
    """`AzureML` Chat models API.

    Example:
        .. code-block:: python

            azure_chat = AzureMLChatOnlineEndpoint(
                endpoint_url="https://<your-endpoint>.<your_region>.inference.ml.azure.com/score",
                endpoint_api_key="my-api-key",
                content_formatter=content_formatter,
            )
    """

    endpoint_url: str = ""
    """URL of pre-existing Endpoint. Should be passed to constructor or specified as 
        env var `AZUREML_ENDPOINT_URL`."""

    endpoint_api_key: SecretStr = convert_to_secret_str("")
    """Authentication Key for Endpoint. Should be passed to constructor or specified as
        env var `AZUREML_ENDPOINT_API_KEY`."""

    http_client: Any = None  #: :meta private:

    content_formatter: Any = None
    """The content formatter that provides an input and output
    transform function to handle formats between the LLM and
    the endpoint"""

    model_kwargs: Optional[dict] = None
    """Keyword arguments to pass to the model."""

    @validator("http_client", always=True, allow_reuse=True)
    @classmethod
    def validate_client(cls, field_value: Any, values: Dict) -> AzureMLEndpointClient:
        """Validate that api key and python package exist in environment."""
        values["endpoint_api_key"] = convert_to_secret_str(
            get_from_dict_or_env(values, "endpoint_api_key", "AZUREML_ENDPOINT_API_KEY")
        )
        endpoint_url = get_from_dict_or_env(
            values, "endpoint_url", "AZUREML_ENDPOINT_URL"
        )
        http_client = AzureMLEndpointClient(
            endpoint_url, values["endpoint_api_key"].get_secret_value()
        )
        return http_client

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Get the identifying parameters."""
        _model_kwargs = self.model_kwargs or {}
        return {
            **{"model_kwargs": _model_kwargs},
        }

    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "azureml_chat_endpoint"

    def _call(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Call out to an AzureML Managed Online endpoint.
        Args:
            messages: The messages in the conversation with the chat model.
            stop: Optional list of stop words to use when generating.
        Returns:
            The string generated by the model.
        Example:
            .. code-block:: python
                response = azureml_model("Tell me a joke.")
        """
        _model_kwargs = self.model_kwargs or {}

        request_payload = self.content_formatter._format_request_payload(
            messages, _model_kwargs
        )
        response_payload = self.http_client.call(request_payload, **kwargs)
        generated_text = self.content_formatter.format_response_payload(
            response_payload
        )
        return generated_text
