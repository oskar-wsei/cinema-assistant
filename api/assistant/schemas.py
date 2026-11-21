from datetime import datetime
from typing import Annotated

from pydantic import Field, StringConstraints

from ..schemas.common import ApiModel


class Conversation(ApiModel):
    id: str = Field(description='The unique identifier of the conversation.')
    created_at: datetime = Field(
        description='The creation timestamp of the conversation.'
    )


class Message(ApiModel):
    id: str = Field(description='The unique identifier of the message.')
    role: str = Field(description='The role of the message sender.')
    content: str = Field(description='The content of the message.')
    created_at: datetime = Field(description='The creation timestamp of the message.')


class MessageCreate(ApiModel):
    content: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=2000)
    ] = Field(description='The content of the message.')
