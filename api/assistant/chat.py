import json
from collections.abc import Iterator
from datetime import datetime, timedelta
from typing import Any

import toon_format

from .ollama import (
    ContentDelta,
    OllamaClient,
    ThinkingDelta,
    ToolCall,
)
from .store import Conversation, Message
from .tools import TOOLS, ToolError

_SYSTEM_PROMPT_TEMPLATE = """You are a helpful assistant in Cinema City application.
Current date and time: {now}. Tomorrow is {tomorrow}."""


class Chat:
    def __init__(self, conversation: Conversation, messages: list[Message]):
        self.conversation = conversation
        self.messages = messages
        self.client = OllamaClient()

    def send_message(self, message: Message) -> Iterator[dict]:
        self.messages.append(message)

        system_message = self._build_system_message()

        while True:
            messages = [
                {'role': 'system', 'content': system_message},
                *[msg.schema() for msg in self.messages],
            ]

            generator = self.client.stream_chat(messages=messages, tools=TOOLS)

            for event in generator:
                if isinstance(event, ContentDelta):
                    yield {'type': 'content', 'text': event.text}
                elif isinstance(event, ThinkingDelta):
                    yield {'type': 'thinking', 'text': event.text}
                else:
                    if event.content:
                        assistant_message = Message(
                            role='assistant',
                            content=event.content,
                            tool_calls=[tc.schema() for tc in event.tool_calls],
                        )
                        self.messages.append(assistant_message)
                        yield {'type': 'completion'}

                    if not event.tool_calls:
                        return

                    for tool_call in event.tool_calls:
                        yield {
                            'type': 'tool_call',
                            'name': tool_call.name,
                            'arguments': tool_call.arguments,
                        }
                        result = self._execute_tool(tool_call)
                        tool_message = Message(
                            role='tool',
                            content=toon_format.dumps(result),
                            tool_name=tool_call.name,
                        )
                        self.messages.append(tool_message)

    def _build_system_message(self) -> str:
        now = datetime.now()
        tomorrow = now + timedelta(days=1)

        system_message = _SYSTEM_PROMPT_TEMPLATE.format(
            now=now.strftime('%A, %Y-%m-%d %H:%M'),
            tomorrow=tomorrow.strftime('%A, %Y-%m-%d'),
        )
        return system_message

    def _execute_tool(self, tool_call: ToolCall) -> Any:
        tool = next((t for t in TOOLS if t.name == tool_call.name), None)
        if tool is None:
            return {'error': f'Unknown tool {tool_call.name!r}.'}
        args = tool_call.arguments or {}
        if isinstance(args, str):
            args = json.loads(args)
        try:
            return tool.execute(args)
        except ToolError as error:
            return {'error': str(error)}
        except KeyError as error:
            return {'error': f'Missing required argument {error}.'}
