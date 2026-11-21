from collections.abc import Iterator
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.sse import EventSourceResponse

from .chat import Chat
from .schemas import (
    Conversation as ConversationSchema,
)
from .schemas import (
    Message as MessageSchema,
)
from .schemas import (
    MessageCreate,
)
from .store import CONVERSATIONS, Conversation, Message

router = APIRouter(prefix='/chat', tags=['Chat'])


def get_conversation_or_404(conversation_id: str) -> Conversation:
    conversation = CONVERSATIONS.get(conversation_id)
    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Conversation not found'
        )
    return conversation


ExistingConversation = Annotated[Conversation, Depends(get_conversation_or_404)]


def get_chat_or_404(conversation_id: str) -> Chat:
    conversation = get_conversation_or_404(conversation_id)
    return Chat(conversation=conversation, messages=conversation.messages)


ExistingChat = Annotated[Chat, Depends(get_chat_or_404)]


@router.post('/conversations', status_code=201, summary='Create a new conversation')
def create_conversation() -> ConversationSchema:
    conversation = Conversation()
    CONVERSATIONS[conversation.id] = conversation
    return conversation


@router.get('/conversations/{conversation_id}', summary='Get a conversation')
def get_conversation(conversation: ExistingConversation) -> ConversationSchema:
    return conversation


@router.get(
    '/conversations/{conversation_id}/messages',
    summary='List messages for a conversation',
)
def list_messages(conversation: ExistingConversation) -> list[MessageSchema]:
    return conversation.messages


@router.post(
    '/conversations/{conversation_id}/messages',
    response_class=EventSourceResponse,
    summary='Create a new message for a conversation',
)
def create_message(chat: ExistingChat, body: MessageCreate) -> Iterator[dict]:
    message = Message(role='user', content=body.content)
    yield from chat.send_message(message)
