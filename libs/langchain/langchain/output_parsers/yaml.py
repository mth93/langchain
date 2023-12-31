import json
import re
from typing import Type, TypeVar

import yaml
from libs.core.langchain_core.exceptions import OutputParserException
from libs.core.langchain_core.output_parsers import BaseOutputParser
from libs.core.langchain_core.pydantic_v1 import BaseModel, ValidationError

from langchain.output_parsers.format_instructions import YAML_FORMAT_INSTRUCTIONS

T = TypeVar("T", bound=BaseModel)


class YamlOutputParser(BaseOutputParser[T]):
    """Parse YAML output using a pydantic model."""

    pydantic_object: Type[T]
    """The pydantic model to parse."""
    pattern: re.Pattern = re.compile(
        r"^```(?:ya?ml)?(?P<yaml>[^`]*)", re.MULTILINE | re.DOTALL
    )
    """Regex pattern to match yaml code blocks 
    within triple backticks with optional yaml or yml prefix."""

    def parse(self, text: str) -> T:
        try:
            # Greedy search for 1st yaml candidate.
            match = re.search(self.pattern, text.strip())
            yaml_str = ""
            if match:
                yaml_str = match.group("yaml")

            json_object = yaml.safe_load(yaml_str)
            return self.pydantic_object.parse_obj(json_object)

        except (yaml.YAMLError, ValidationError) as e:
            name = self.pydantic_object.__name__
            msg = f"Failed to parse {name} from completion {text}. Got: {e}"
            raise OutputParserException(msg, llm_output=text)

    def get_format_instructions(self) -> str:
        schema = self.pydantic_object.schema()

        # Remove extraneous fields.
        reduced_schema = schema
        if "title" in reduced_schema:
            del reduced_schema["title"]
        if "type" in reduced_schema:
            del reduced_schema["type"]
        # Ensure yaml in context is well-formed with double quotes.
        schema_str = json.dumps(reduced_schema)

        return YAML_FORMAT_INSTRUCTIONS.format(schema=schema_str)

    @property
    def _type(self) -> str:
        return "yaml"
