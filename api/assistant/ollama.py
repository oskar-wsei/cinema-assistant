from dataclasses import dataclass

from ollama import Client

from .tool import Tool, ToolCall


@dataclass
class ContentDelta:
    text: str


@dataclass
class ThinkingDelta:
    text: str


@dataclass
class Completion:
    content: str
    thinking: str
    tool_calls: list[ToolCall]


class OllamaClient:
    def __init__(self):
        self.client = Client(host='http://localhost:11434')

    def stream_chat(
        self,
        messages: list[dict[str, str]] | None = None,
        tools: list[Tool] | None = None,
    ):
        generator = self.client.chat(
            model='qwen3.5:2b',
            messages=messages,
            tools=[tool.schema() for tool in tools] if tools else None,
            stream=True,
            think=False,
            options={'num_ctx': 16384},
        )

        content = ''
        thinking = ''
        tool_calls: list[ToolCall] = []

        for chunk in generator:
            if chunk.done:
                break

            if chunk.message.content:
                content += chunk.message.content
                yield ContentDelta(text=chunk.message.content)

            if chunk.message.thinking:
                thinking += chunk.message.thinking
                yield ThinkingDelta(text=chunk.message.thinking)

            if chunk.message.tool_calls:
                for tool_call in chunk.message.tool_calls:
                    tool_calls.append(
                        ToolCall(
                            name=tool_call.function.name,
                            arguments=tool_call.function.arguments,
                        )
                    )

        yield Completion(content=content, thinking=thinking, tool_calls=tool_calls)
