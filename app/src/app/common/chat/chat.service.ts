import { HttpClient } from '@angular/common/http';
import { Service, inject } from '@angular/core';
import { firstValueFrom } from 'rxjs';

import { Conversation, MessageCreate } from '../../types/api.types';
import { API_URL } from '../api';

export type ChatEvent =
  | { type: 'content'; text: string }
  | { type: 'thinking'; text: string }
  | { type: 'tool_call'; name: string; arguments: Record<string, unknown> }
  | { type: 'completion' };

export class ChatRequestError extends Error {
  public constructor(public readonly status: number) {
    super(`Chat request failed with status ${status}`);
  }
}

@Service()
export class ChatService {
  private readonly http = inject(HttpClient);

  public createConversation(): Promise<Conversation> {
    return firstValueFrom(this.http.post<Conversation>(`${API_URL}/chat/conversations`, null));
  }

  public async *sendMessage(conversationId: string, content: string): AsyncGenerator<ChatEvent> {
    const response = await fetch(
      `${API_URL}/chat/conversations/${encodeURIComponent(conversationId)}/messages`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'text/event-stream' },
        body: JSON.stringify({ content } satisfies MessageCreate),
      },
    );
    if (!response.ok || !response.body) throw new ChatRequestError(response.status);

    const reader = response.body.pipeThrough(new TextDecoderStream()).getReader();
    let buffer = '';
    while (true) {
      const { done, value } = await reader.read();
      if (done) return;

      buffer += value.replaceAll('\r\n', '\n');
      const blocks = buffer.split('\n\n');
      buffer = blocks.pop() ?? '';
      for (const block of blocks) {
        const event = this.parseEvent(block);
        if (event) yield event;
      }
    }
  }

  private parseEvent(block: string): ChatEvent | null {
    const data = block
      .split('\n')
      .filter((line) => line.startsWith('data:'))
      .map((line) => line.slice('data:'.length).trimStart())
      .join('\n');
    return data ? (JSON.parse(data) as ChatEvent) : null;
  }
}
