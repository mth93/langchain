"""BasePrompt schema definition."""
from __future__ import annotations

import warnings
from abc import ABC
from string import Formatter
from typing import Any, Callable, Dict, List, Set

from langchain.libs.core.langchain_core.prompt_values import PromptValue, StringPromptValue
from langchain.libs.core.langchain_core.prompts.base import BasePromptTemplate
from langchain.libs.core.langchain_core.utils.formatting import formatter


def jinja2_formatter(template: str, **kwargs: Any) -> str:
    """Format a template using jinja2.

    *Security warning*: As of LangChain 0.0.329, this method uses Jinja2's
        SandboxedEnvironment by default. However, this sand-boxing should
        be treated as a best-effort approach rather than a guarantee of security.
        Do not accept jinja2 templates from untrusted sources as they may lead
        to arbitrary Python code execution.

        https://jinja.palletsprojects.com/en/3.1.x/sandbox/
    """
    try:
        from jinja2.sandbox import SandboxedEnvironment
    except ImportError:
        raise ImportError(
            "jinja2 not installed, which is needed to use the jinja2_formatter. "
            "Please install it with `pip install jinja2`."
            "Please be cautious when using jinja2 templates. "
            "Do not expand jinja2 templates using unverified or user-controlled "
            "inputs as that can result in arbitrary Python code execution."
        )

    # This uses a sandboxed environment to prevent arbitrary code execution.
    # Jinja2 uses an opt-out rather than opt-in approach for sand-boxing.
    # Please treat this sand-boxing as a best-effort approach rather than
    # a guarantee of security.
    # We recommend to never use jinja2 templates with untrusted inputs.
    # https://jinja.palletsprojects.com/en/3.1.x/sandbox/
    # approach not a guarantee of security.
    return SandboxedEnvironment().from_string(template).render(**kwargs)


def validate_jinja2(template: str, input_variables: List[str]) -> None:
    """
    Validate that the input variables are valid for the template.
    Issues a warning if missing or extra variables are found.

    Args:
        template: The template string.
        input_variables: The input variables.
    """
    input_variables_set = set(input_variables)
    valid_variables = _get_jinja2_variables_from_template(template)
    missing_variables = valid_variables - input_variables_set
    extra_variables = input_variables_set - valid_variables

    warning_message = ""
    if missing_variables:
        warning_message += f"Missing variables: {missing_variables} "

    if extra_variables:
        warning_message += f"Extra variables: {extra_variables}"

    if warning_message:
        warnings.warn(warning_message.strip())


def _get_jinja2_variables_from_template(template: str) -> Set[str]:
    try:
        from jinja2 import Environment, meta
    except ImportError:
        raise ImportError(
            "jinja2 not installed, which is needed to use the jinja2_formatter. "
            "Please install it with `pip install jinja2`."
        )
    env = Environment()
    ast = env.parse(template)
    variables = meta.find_undeclared_variables(ast)
    return variables


DEFAULT_FORMATTER_MAPPING: Dict[str, Callable] = {
    "f-string": formatter.format,
    "jinja2": jinja2_formatter,
}

DEFAULT_VALIDATOR_MAPPING: Dict[str, Callable] = {
    "f-string": formatter.validate_input_variables,
    "jinja2": validate_jinja2,
}


def check_valid_template(
    template: str, template_format: str, input_variables: List[str]
) -> None:
    """Check that template string is valid.

    Args:
        template: The template string.
        template_format: The template format. Should be one of "f-string" or "jinja2".
        input_variables: The input variables.

    Raises:
        ValueError: If the template format is not supported.
    """
    try:
        validator_func = DEFAULT_VALIDATOR_MAPPING[template_format]
    except KeyError as exc:
        raise ValueError(
            f"Invalid template format {template_format!r}, should be one of"
            f" {list(DEFAULT_FORMATTER_MAPPING)}."
        ) from exc
    try:
        validator_func(template, input_variables)
    except (KeyError, IndexError) as exc:
        raise ValueError(
            "Invalid prompt schema; check for mismatched or missing input parameters"
            f" from {input_variables}."
        ) from exc


def get_template_variables(template: str, template_format: str) -> List[str]:
    """Get the variables from the template.

    Args:
        template: The template string.
        template_format: The template format. Should be one of "f-string" or "jinja2".

    Returns:
        The variables from the template.

    Raises:
        ValueError: If the template format is not supported.
    """
    if template_format == "jinja2":
        # Get the variables for the template
        input_variables = _get_jinja2_variables_from_template(template)
    elif template_format == "f-string":
        input_variables = {
            v for _, v, _, _ in Formatter().parse(template) if v is not None
        }
    else:
        raise ValueError(f"Unsupported template format: {template_format}")

    return sorted(input_variables)


class StringPromptTemplate(BasePromptTemplate, ABC):
    """String prompt that exposes the format method, returning a prompt."""

    @classmethod
    def get_lc_namespace(cls) -> List[str]:
        """Get the namespace of the langchain object."""
        return ["langchain", "prompts", "base"]

    def format_prompt(self, **kwargs: Any) -> PromptValue:
        """Create Chat Messages."""
        return StringPromptValue(text=self.format(**kwargs))
