import { DOCUMENT, DatePipe } from '@angular/common';
import { Component, computed, effect, inject, input, resource } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';

import {
  ageRatingLabel,
  durationLabel,
  formatLabels,
  genreLabel,
  languageName,
} from '../../common/movie/movie-labels';
import { MovieService } from '../../common/movie/movie.service';
import { Trailer } from '../../common/movie/trailer/trailer';
import {
  MovieScreenings,
  ScreeningsSelection,
} from '../../common/screening/movie-screenings/movie-screenings';

@Component({
  selector: 'app-movie',
  imports: [DatePipe, MovieScreenings, RouterLink, Trailer],
  templateUrl: 'movie.page.html',
  styleUrl: 'movie.page.scss',
})
export default class MoviePage {
  public readonly movieId = input.required<string>();
  public readonly city = input<string>();
  public readonly date = input<string>();

  private readonly movieService = inject(MovieService);
  private readonly router = inject(Router);
  private readonly route = inject(ActivatedRoute);
  private readonly document = inject(DOCUMENT);

  protected readonly movie = resource({
    params: () => this.movieId(),
    loader: ({ params: movieId }) => this.movieService.get(movieId),
  });

  /** The movie with its display-ready labels, or `null` if it does not exist. */
  protected readonly view = computed(() => {
    const movie = this.movie.value();
    if (!movie) return null;
    return {
      movie,
      duration: movie.duration_minutes && durationLabel(movie.duration_minutes),
      ageRating: ageRatingLabel(movie.age_rating.code),
      genres: movie.genres.map(genreLabel).join(', '),
      formats: formatLabels(movie.attributes),
      originalLanguages: movie.languages.original.map(languageName).join(', '),
      production: [movie.release_country, movie.release_year].filter(Boolean).join(' '),
    };
  });

  public constructor() {
    const title = inject(Title);
    effect(() => {
      const movie = this.movie.value();
      if (movie) title.setTitle(`${movie.title} - Cinema City`);
    });
  }

  protected scrollTo(sectionId: string): void {
    this.document.getElementById(sectionId)?.scrollIntoView({ behavior: 'smooth' });
  }

  protected async showScreenings({ cityId, date }: ScreeningsSelection): Promise<void> {
    await this.router.navigate([], {
      relativeTo: this.route,
      queryParams: { city: cityId, date },
      queryParamsHandling: 'merge',
      replaceUrl: true,
      scroll: 'manual',
    });
  }
}
