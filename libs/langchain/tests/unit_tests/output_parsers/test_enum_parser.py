from enum import Enum

from langchain.libs.core.langchain_core.exceptions import OutputParserException

from langchain.libs.langchain.langchain.output_parsers.enum import EnumOutputParser


class Colors(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


def test_enum_output_parser_parse() -> None:
    parser = EnumOutputParser(enum=Colors)

    # Test valid inputs
    result = parser.parse("red")
    assert result == Colors.RED

    result = parser.parse("green")
    assert result == Colors.GREEN

    result = parser.parse("blue")
    assert result == Colors.BLUE

    # Test invalid input
    try:
        parser.parse("INVALID")
        assert False, "Should have raised OutputParserException"
    except OutputParserException:
        pass
