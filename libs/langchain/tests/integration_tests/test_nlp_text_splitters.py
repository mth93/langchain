"""Test text splitting functionality using NLTK and Spacy based sentence splitters."""
import pytest

from langchain.libs.langchain.langchain.text_splitter import NLTKTextSplitter, SpacyTextSplitter


def test_nltk_text_splitting_args() -> None:
    """Test invalid arguments."""
    with pytest.raises(ValueError):
        NLTKTextSplitter(chunk_size=2, chunk_overlap=4)


def test_spacy_text_splitting_args() -> None:
    """Test invalid arguments."""
    with pytest.raises(ValueError):
        SpacyTextSplitter(chunk_size=2, chunk_overlap=4)


def test_nltk_text_splitter() -> None:
    """Test splitting by sentence using NLTK."""
    text = "This is sentence one. And this is sentence two."
    separator = "|||"
    splitter = NLTKTextSplitter(separator=separator)
    output = splitter.split_text(text)
    expected_output = [f"This is sentence one.{separator}And this is sentence two."]
    assert output == expected_output


@pytest.mark.parametrize("pipeline", ["sentencizer", "en_core_web_sm"])
def test_spacy_text_splitter(pipeline: str) -> None:
    """Test splitting by sentence using Spacy."""
    text = "This is sentence one. And this is sentence two."
    separator = "|||"
    splitter = SpacyTextSplitter(separator=separator, pipeline=pipeline)
    output = splitter.split_text(text)
    expected_output = [f"This is sentence one.{separator}And this is sentence two."]
    assert output == expected_output
