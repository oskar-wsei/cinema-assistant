import { Component, computed, input } from '@angular/core';
import { DatePipe } from '@angular/common';
import { RouterLink } from '@angular/router';

import { Movie } from '../../../types/api.types';
import { localIsoDate } from '../../date.utils';
import { HIGHLIGHTED_FORMATS, formatLabels } from '../movie-labels';

@Component({
  selector: 'app-movie-card',
  imports: [DatePipe, RouterLink],
  templateUrl: 'movie-card.html',
  styleUrl: 'movie-card.scss',
})
export class MovieCard {
  public readonly movie = input.required<Movie>();

  protected readonly formats = computed(() =>
    formatLabels(this.movie().attributes, HIGHLIGHTED_FORMATS),
  );

  protected readonly upcomingRelease = computed(() => {
    const releaseDate = this.movie().release_date;
    return releaseDate && releaseDate > localIsoDate() ? releaseDate : null;
  });
}
