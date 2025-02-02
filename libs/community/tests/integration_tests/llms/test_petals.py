"""Test Petals API wrapper."""

from langchain.libs.core.langchain_core.pydantic_v1 import SecretStr
from pytest import CaptureFixture

from langchain_community.llms.petals import Petals


def test_api_key_is_string() -> None:
    llm = Petals(huggingface_api_key="secret-api-key")
    assert isinstance(llm.huggingface_api_key, SecretStr)


def test_api_key_masked_when_passed_via_constructor(
    capsys: CaptureFixture,
) -> None:
    llm = Petals(huggingface_api_key="secret-api-key")
    print(llm.huggingface_api_key, end="")
    captured = capsys.readouterr()

    assert captured.out == "**********"


def test_gooseai_call() -> None:
    """Test valid call to gooseai."""
    llm = Petals(max_new_tokens=10)
    output = llm("Say foo:")
    assert isinstance(output, str)
