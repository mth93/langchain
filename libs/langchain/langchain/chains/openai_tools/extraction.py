from typing import List, Type, Union

from langchain.libs.core.langchain_core.language_models import BaseLanguageModel
from langchain.libs.core.langchain_core.prompts import ChatPromptTemplate
from langchain.libs.core.langchain_core.pydantic_v1 import BaseModel
from langchain.libs.core.langchain_core.runnables import Runnable

from langchain.libs.langchain.langchain.output_parsers import PydanticToolsParser
from langchain.libs.langchain.langchain.utils.openai_functions import convert_pydantic_to_openai_function

_EXTRACTION_TEMPLATE = """Extract and save the relevant entities mentioned \
in the following passage together with their properties.

If a property is not present and is not required in the function parameters, do not include it in the output."""  # noqa: E501


def create_extraction_chain_pydantic(
    pydantic_schemas: Union[List[Type[BaseModel]], Type[BaseModel]],
    llm: BaseLanguageModel,
    system_message: str = _EXTRACTION_TEMPLATE,
) -> Runnable:
    """Creates a chain that extracts information from a passage.

    Args:
        pydantic_schemas: The schema of the entities to extract.
        llm: The language model to use.
        system_message: The system message to use for extraction.

    Returns:
        A runnable that extracts information from a passage.
    """
    if not isinstance(pydantic_schemas, list):
        pydantic_schemas = [pydantic_schemas]
    prompt = ChatPromptTemplate.from_messages(
        [("system", system_message), ("user", "{input}")]
    )
    functions = [convert_pydantic_to_openai_function(p) for p in pydantic_schemas]
    tools = [{"type": "function", "function": d} for d in functions]
    model = llm.bind(tools=tools)
    chain = prompt | model | PydanticToolsParser(tools=pydantic_schemas)
    return chain
