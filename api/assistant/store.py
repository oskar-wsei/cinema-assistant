from datetime import datetime
from uuid import uuid4


class Conversation:
    def __init__(self):
        self.id = uuid4().hex
        self.created_at = datetime.now()
        self.messages: list[Message] = []


class Message:
    def __init__(
        self,
        role: str,
        content: str,
        tool_calls: list[dict] | None = None,
        tool_name: str | None = None,
    ):
        self.id = uuid4().hex
        self.role = role
        self.content = content
        self.tool_calls = tool_calls
        self.tool_name = tool_name
        self.created_at = datetime.now()

    def schema(self) -> dict:
        return {
            'role': self.role,
            'content': self.content,
            'tool_calls': self.tool_calls,
            'tool_name': self.tool_name
        }


CONVERSATIONS: dict[str, Conversation] = {}
