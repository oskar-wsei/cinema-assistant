import { Component, computed, inject, input, signal } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-trailer',
  templateUrl: 'trailer.html',
  styleUrl: 'trailer.scss',
})
export class Trailer {
  private readonly sanitizer = inject(DomSanitizer);

  public readonly url = input.required<string>();
  public readonly title = input.required<string>();

  private readonly reYoutubeVideoId = /(?:youtube\.com\/(?:watch\?v=|embed\/)|youtu\.be\/)([\w-]{11})/;

  protected readonly playing = signal(false);
  protected readonly videoId = computed(() => this.reYoutubeVideoId.exec(this.url())?.[1] ?? null);

  protected readonly thumbnailUrl = computed(
    () => `https://i.ytimg.com/vi/${this.videoId()}/hqdefault.jpg`,
  );

  protected readonly embedUrl = computed<SafeResourceUrl>(() =>
    this.sanitizer.bypassSecurityTrustResourceUrl(
      `https://www.youtube-nocookie.com/embed/${this.videoId()}?autoplay=1&rel=0`,
    ),
  );
}
