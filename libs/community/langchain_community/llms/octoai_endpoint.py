from typing import Any, Dict, List, Mapping, Optional

from langchain.libs.core.langchain_core.callbacks import CallbackManagerForLLMRun
from langchain.libs.core.langchain_core.language_models.llms import LLM
from langchain.libs.core.langchain_core.pydantic_v1 import Extra, root_validator
from langchain.libs.core.langchain_core.utils import get_from_dict_or_env

from langchain_community.llms.utils import enforce_stop_tokens


class OctoAIEndpoint(LLM):
    """OctoAI LLM Endpoints.

    OctoAIEndpoint is a class to interact with OctoAI
     Compute Service large language model endpoints.

    To use, you should have the ``octoai`` python package installed, and the
    environment variable ``OCTOAI_API_TOKEN`` set with your API token, or pass
    it as a named parameter to the constructor.

    Example:
        .. code-block:: python

            from langchain_community.llms.octoai_endpoint  import OctoAIEndpoint
            OctoAIEndpoint(
                octoai_api_token="octoai-api-key",
                endpoint_url="https://mpt-7b-demo-f1kzsig6xes9.octoai.run/generate",
                model_kwargs={
                    "max_new_tokens": 200,
                    "temperature": 0.75,
                    "top_p": 0.95,
                    "repetition_penalty": 1,
                    "seed": None,
                    "stop": [],
                },
            )

            from langchain_community.llms.octoai_endpoint  import OctoAIEndpoint
            OctoAIEndpoint(
                octoai_api_token="octoai-api-key",
                endpoint_url="https://llama-2-7b-chat-demo-kk0powt97tmb.octoai.run/v1/chat/completions",
                model_kwargs={
                    "model": "llama-2-7b-chat",
                    "messages": [
                        {
                            "role": "system",
                            "content": "Below is an instruction that describes a task.
                                Write a response that completes the request."
                        }
                    ],
                    "stream": False,
                    "max_tokens": 256
                }
            )

    """

    endpoint_url: Optional[str] = None
    """Endpoint URL to use."""

    model_kwargs: Optional[dict] = None
    """Keyword arguments to pass to the model."""

    octoai_api_token: Optional[str] = None
    """OCTOAI API Token"""

    streaming: bool = False
    """Whether to generate a stream of tokens asynchronously"""

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    @root_validator(allow_reuse=True)
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and python package exists in environment."""
        octoai_api_token = get_from_dict_or_env(
            values, "octoai_api_token", "OCTOAI_API_TOKEN"
        )
        values["endpoint_url"] = get_from_dict_or_env(
            values, "endpoint_url", "ENDPOINT_URL"
        )

        values["octoai_api_token"] = octoai_api_token
        return values

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        _model_kwargs = self.model_kwargs or {}
        return {
            **{"endpoint_url": self.endpoint_url},
            **{"model_kwargs": _model_kwargs},
        }

    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "octoai_endpoint"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Call out to OctoAI's inference endpoint.

        Args:
            prompt: The prompt to pass into the model.
            stop: Optional list of stop words to use when generating.

        Returns:
            The string generated by the model.

        """
        _model_kwargs = self.model_kwargs or {}

        try:
            # Initialize the OctoAI client
            from octoai import client

            octoai_client = client.Client(token=self.octoai_api_token)

            if "model" in _model_kwargs:
                parameter_payload = _model_kwargs
                parameter_payload["messages"].append(
                    {"role": "user", "content": prompt}
                )
                # Send the request using the OctoAI client
                output = octoai_client.infer(self.endpoint_url, parameter_payload)
                text = output.get("choices")[0].get("message").get("content")
            else:
                # Prepare the payload JSON
                parameter_payload = {"inputs": prompt, "parameters": _model_kwargs}

                # Send the request using the OctoAI client
                resp_json = octoai_client.infer(self.endpoint_url, parameter_payload)
                text = resp_json["generated_text"]

        except Exception as e:
            # Handle any errors raised by the inference endpoint
            raise ValueError(f"Error raised by the inference endpoint: {e}") from e

        if stop is not None:
            # Apply stop tokens when making calls to OctoAI
            text = enforce_stop_tokens(text, stop)

        return text
