from dataclasses import dataclass
from typing import Any


@dataclass
class ToolCall:
    name: str
    arguments: dict[str, Any] | str

    def schema(self) -> dict[str, Any]:
        return {
            'function': {
                'name': self.name,
                'arguments': self.arguments,
            }
        }


@dataclass
class Tool:
    name: str
    description: str
    parameters: dict[str, Any] | None = None

    def schema(self) -> dict[str, Any]:
        return type_function(
            name=self.name,
            description=self.description,
            parameters=self.parameters or type_object(),
        )

    def execute(self, args: dict[str, Any]) -> dict:
        raise NotImplementedError


def type_function(
    name: str,
    description: str,
    parameters: dict[str, Any],
):
    return {
        'type': 'function',
        'function': {
            'name': name,
            'description': description,
            'parameters': parameters,
        },
    }


def type_object(
    required: dict[str, Any] | None = None,
    optional: dict[str, Any] | None = None,
):
    required = required or {}
    optional = optional or {}
    return {
        'type': 'object',
        'properties': {**required, **optional},
        'required': list(required.keys()),
        'additionalProperties': False,
    }


def type_string(description: str, enum: list[str] | None = None) -> dict[str, Any]:
    schema: dict[str, Any] = {'type': 'string', 'description': description}
    if enum:
        schema['enum'] = enum
    return schema
