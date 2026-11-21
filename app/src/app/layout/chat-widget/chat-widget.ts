import {
  Component,
  ElementRef,
  Injector,
  afterNextRender,
  afterRenderEffect,
  computed,
  inject,
  signal,
  viewChild,
} from '@angular/core';

import { ChatRequestError, ChatService } from '../../common/chat/chat.service';

interface ChatMessage {
  id: number;
  role: 'user' | 'assistant';
  content: string;
}

@Component({
  selector: 'app-chat-widget',
  templateUrl: 'chat-widget.html',
  styleUrl: 'chat-widget.scss',
})
export class ChatWidget {
  private readonly chatService = inject(ChatService);
  private readonly injector = inject(Injector);

  private readonly toolLabels: Record<string, string> = {
    list_cinemas: 'Sprawdzam listę kin…',
    list_movies: 'Przeglądam repertuar…',
    get_movie_details: 'Sprawdzam szczegóły filmu…',
    list_movie_screenings: 'Szukam seansów filmu…',
    list_cinema_screenings: 'Sprawdzam repertuar kina…',
  };

  /** Kept in memory only, so a page refresh starts a new conversation. */
  private conversationId: string | null = null;
  private nextMessageId = 0;

  protected readonly maxLength = 2000;
  protected readonly isOpen = signal(false);
  protected readonly messages = signal<ChatMessage[]>([]);
  protected readonly draft = signal('');
  protected readonly sending = signal(false);
  protected readonly failed = signal(false);
  private readonly activeTool = signal<string | null>(null);
  private readonly replyId = signal<number | null>(null);

  protected readonly canSend = computed(() => !this.sending() && !!this.draft().trim());

  /** What the assistant is doing while no reply text has arrived yet. */
  protected readonly status = computed(() => {
    if (!this.sending()) return null;
    const tool = this.activeTool();
    if (tool) return this.toolLabels[tool] ?? 'Szukam informacji…';
    return this.replyId() === null ? 'Piszę odpowiedź…' : null;
  });

  private readonly messageList = viewChild<ElementRef<HTMLElement>>('messageList');
  private readonly input = viewChild<ElementRef<HTMLTextAreaElement>>('input');
  private readonly bubble = viewChild<ElementRef<HTMLButtonElement>>('bubble');

  public constructor() {
    afterRenderEffect(() => {
      this.messages();
      this.status();
      this.failed();
      const list = this.messageList()?.nativeElement;
      if (list) list.scrollTop = list.scrollHeight;
    });
  }

  protected open(): void {
    this.isOpen.set(true);
    afterNextRender(() => this.input()?.nativeElement.focus(), { injector: this.injector });
  }

  protected close(): void {
    this.isOpen.set(false);
    afterNextRender(() => this.bubble()?.nativeElement.focus(), { injector: this.injector });
  }

  protected submitOnEnter(event: Event): void {
    if (!(event instanceof KeyboardEvent) || event.shiftKey || event.isComposing) return;
    event.preventDefault();
    void this.send();
  }

  protected async send(): Promise<void> {
    const content = this.draft().trim();
    if (!this.canSend()) return;

    this.draft.set('');
    this.failed.set(false);
    this.sending.set(true);
    let userMessage = this.addMessage('user', content);

    try {
      try {
        await this.streamReply(content);
      } catch (error) {
        if (!(error instanceof ChatRequestError && error.status === 404)) throw error;
        this.conversationId = null;
        this.messages.set([]);
        userMessage = this.addMessage('user', content);
        await this.streamReply(content);
      }
    } catch {
      if (this.replyId() === null && !this.draft().trim()) {
        this.messages.update((messages) => messages.filter((m) => m !== userMessage));
        this.draft.set(content);
      }
      this.failed.set(true);
    } finally {
      this.sending.set(false);
      this.activeTool.set(null);
      this.replyId.set(null);
    }
  }

  private async streamReply(content: string): Promise<void> {
    this.conversationId ??= (await this.chatService.createConversation()).id;
    for await (const event of this.chatService.sendMessage(this.conversationId, content)) {
      if (event.type === 'tool_call') {
        this.activeTool.set(event.name);
      } else if (event.type === 'content') {
        this.activeTool.set(null);
        this.appendToReply(event.text);
      }
    }
    if (this.replyId() === null) throw new Error('The assistant sent no reply');
  }

  private addMessage(role: ChatMessage['role'], content: string): ChatMessage {
    const message = { id: this.nextMessageId++, role, content };
    this.messages.update((messages) => [...messages, message]);
    return message;
  }

  private appendToReply(text: string): void {
    const replyId = this.replyId();
    if (replyId === null) {
      this.replyId.set(this.addMessage('assistant', text).id);
      return;
    }
    this.messages.update((messages) =>
      messages.map((m) => (m.id === replyId ? { ...m, content: m.content + text } : m)),
    );
  }
}
