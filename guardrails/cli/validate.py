import json
from typing import Dict, Union

import typer

from guardrails import Guard
from guardrails.cli.guardrails import guardrails


def validate_llm_output(rail: str, llm_output: str) -> Union[str, Dict, None]:
    """Validate guardrails.yml file."""
    guard = Guard.from_rail(rail)
    result = guard.parse(llm_output)
    return result.validated_output


@guardrails.command()
def validate(
    rail: str = typer.Argument(
        ..., help="Path to the rail spec.", exists=True, file_okay=True, dir_okay=False
    ),
    llm_output: str = typer.Argument(..., help="String of llm output."),
    out: str = typer.Option(
        default=".rail_output",
        help="Path to the compiled output directory.",
        file_okay=True,
        dir_okay=False,
    ),
):
    """Validate the output of an LLM against a `rail` spec."""
    result = validate_llm_output(rail, llm_output)
    # Result is a dictionary, log it to a file
    print(result)

    with open(out, "w") as f:
        json.dump(result, f)
        f.write("\n")

    return result
