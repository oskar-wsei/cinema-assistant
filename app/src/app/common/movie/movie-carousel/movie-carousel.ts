import {
  Component,
  DestroyRef,
  ElementRef,
  afterNextRender,
  inject,
  input,
  signal,
  viewChild,
} from '@angular/core';

import { Movie } from '../../../types/api.types';
import { MovieCard } from '../movie-card/movie-card';

@Component({
  selector: 'app-movie-carousel',
  imports: [MovieCard],
  templateUrl: 'movie-carousel.html',
  styleUrl: 'movie-carousel.scss',
})
export class MovieCarousel {
  private static nextId = 0;

  public readonly heading = input.required<string>();
  public readonly movies = input.required<Movie[]>();

  private readonly pageScrollRatio = 0.85;

  protected readonly headingId = `movie-carousel-${MovieCarousel.nextId++}`;
  protected readonly canScrollBack = signal(false);
  protected readonly canScrollForward = signal(false);

  private readonly track = viewChild.required<ElementRef<HTMLElement>>('track');

  public constructor() {
    const destroyRef = inject(DestroyRef);

    afterNextRender(() => {
      const observer = new ResizeObserver(() => this.updateScrollState());
      observer.observe(this.track().nativeElement);
      destroyRef.onDestroy(() => observer.disconnect());
    });
  }

  protected scrollPage(direction: -1 | 1): void {
    const track = this.track().nativeElement;
    track.scrollBy({
      left: direction * track.clientWidth * this.pageScrollRatio,
      behavior: 'smooth',
    });
  }

  protected updateScrollState(): void {
    const { scrollLeft, scrollWidth, clientWidth } = this.track().nativeElement;
    this.canScrollBack.set(scrollLeft > 1);
    this.canScrollForward.set(scrollLeft + clientWidth < scrollWidth - 1);
  }
}
