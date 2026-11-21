import { Component, computed, inject, input, output, resource } from '@angular/core';

import { City } from '../../../types/api.types';
import { CityPreference } from '../../city/city-preference.service';
import { MovieService } from '../../movie/movie.service';
import { CinemaShowtimes } from '../cinema-showtimes/cinema-showtimes';
import { DayPicker } from '../day-picker/day-picker';

export interface ScreeningsSelection {
  cityId: string;
  date: string | null;
}

@Component({
  selector: 'app-movie-screenings',
  imports: [CinemaShowtimes, DayPicker],
  templateUrl: 'movie-screenings.html',
  styleUrl: 'movie-screenings.scss',
})
export class MovieScreenings {
  public readonly movieId = input.required<string>();
  public readonly city = input<string>();
  public readonly date = input<string>();
  public readonly selectionChange = output<ScreeningsSelection>();

  private readonly movieService = inject(MovieService);
  private readonly cityPreference = inject(CityPreference);

  protected readonly cities = resource({
    params: () => this.movieId(),
    loader: ({ params: movieId }) => this.movieService.cities(movieId),
  });

  protected readonly selectedCity = computed<City | undefined>(() => {
    if (!this.cities.hasValue()) {
      return undefined;
    }
    const cities = this.cities.value();
    const findCity = (cityId?: string) => cities.find((city) => city.id === cityId);
    return findCity(this.city()) ?? findCity(this.cityPreference.cityId()) ?? cities[0];
  });

  protected readonly days = resource({
    params: () => {
      const city = this.selectedCity();
      return city ? { movieId: this.movieId(), cityId: city.id } : undefined;
    },
    loader: ({ params }) => this.movieService.screeningDates(params.movieId, params.cityId),
  });

  protected readonly selectedDay = computed(() => {
    if (!this.days.hasValue()) {
      return undefined;
    }
    const days = this.days.value();
    const requested = this.date();
    return requested && days.includes(requested) ? requested : days[0];
  });

  protected readonly screenings = resource({
    params: () => {
      const city = this.selectedCity();
      const date = this.selectedDay();
      return city && date ? { movieId: this.movieId(), cityId: city.id, date } : undefined;
    },
    loader: ({ params }) =>
      this.movieService.screenings(params.movieId, params.cityId, params.date),
  });

  protected selectCity(cityId: string): void {
    this.cityPreference.set(cityId);
    this.selectionChange.emit({ cityId, date: null });
  }

  protected selectDay(date: string): void {
    const city = this.selectedCity();
    if (city) {
      this.selectionChange.emit({ cityId: city.id, date });
    }
  }

  protected retry(): void {
    for (const step of [this.cities, this.days, this.screenings]) {
      if (step.error()) {
        step.reload();
        return;
      }
    }
  }
}
