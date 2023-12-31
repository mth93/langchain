"""Wrapper around Minimax chat models."""
import logging
from typing import Any, Dict, List, Optional, cast

from libs.core.langchain_core.callbacks import (
    AsyncCallbackManagerForLLMRun,
    CallbackManagerForLLMRun,
)
from libs.core.langchain_core.language_models.chat_models import BaseChatModel
from libs.core.langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
)
from libs.core.langchain_core.outputs import ChatResult

from langchain_community.llms.minimax import MinimaxCommon
from langchain_community.llms.utils import enforce_stop_tokens

logger = logging.getLogger(__name__)


def _parse_message(msg_type: str, text: str) -> Dict:
    return {"sender_type": msg_type, "text": text}


def _parse_chat_history(history: List[BaseMessage]) -> List:
    """Parse a sequence of messages into history."""
    chat_history = []
    for message in history:
        content = cast(str, message.content)
        if isinstance(message, HumanMessage):
            chat_history.append(_parse_message("USER", content))
        if isinstance(message, AIMessage):
            chat_history.append(_parse_message("BOT", content))
    return chat_history


class MiniMaxChat(MinimaxCommon, BaseChatModel):
    """Wrapper around Minimax large language models.

    To use, you should have the environment variable ``MINIMAX_GROUP_ID`` and
    ``MINIMAX_API_KEY`` set with your API token, or pass it as a named parameter to
    the constructor.

    Example:
        .. code-block:: python

            from langchain_community.chat_models import MiniMaxChat
            llm = MiniMaxChat(model_name="abab5-chat")

    """

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Generate next turn in the conversation.
        Args:
            messages: The history of the conversation as a list of messages. Code chat
                does not support context.
            stop: The list of stop words (optional).
            run_manager: The CallbackManager for LLM run, it's not used at the moment.

        Returns:
            The ChatResult that contains outputs generated by the model.

        Raises:
            ValueError: if the last message in the list is not from human.
        """
        if not messages:
            raise ValueError(
                "You should provide at least one message to start the chat!"
            )
        history = _parse_chat_history(messages)
        payload = self._default_params
        payload["messages"] = history
        text = self._client.post(payload)

        # This is required since the stop are not enforced by the model parameters
        return text if stop is None else enforce_stop_tokens(text, stop)

    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        raise NotImplementedError(
            """Minimax AI doesn't support async requests at the moment."""
        )
