import { Component, computed, input } from '@angular/core';
import { DatePipe, PercentPipe } from '@angular/common';

import { CinemaScreenings, Screening } from '../../../types/api.types';
import { groupByVersion } from '../screening-versions';

@Component({
  selector: 'app-cinema-showtimes',
  imports: [DatePipe, PercentPipe],
  templateUrl: 'cinema-showtimes.html',
  styleUrl: 'cinema-showtimes.scss',
})
export class CinemaShowtimes {
  public readonly cinemaScreenings = input.required<CinemaScreenings>();

  private readonly fewSeatsLeft = 0.15;

  protected readonly cinema = computed(() => this.cinemaScreenings().cinema);
  protected readonly versions = computed(() => groupByVersion(this.cinemaScreenings().screenings));

  protected isBookable(screening: Screening): boolean {
    return !screening.sold_out && new Date(screening.starts_at) > new Date();
  }

  protected hasFewSeatsLeft(screening: Screening): boolean {
    return screening.seat_availability < this.fewSeatsLeft;
  }
}
