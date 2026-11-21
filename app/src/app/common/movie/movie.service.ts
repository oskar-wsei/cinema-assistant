import { HttpClient, HttpErrorResponse, HttpStatusCode } from '@angular/common/http';
import { Service, inject } from '@angular/core';
import { firstValueFrom } from 'rxjs';

import { CinemaScreenings, City, MovieDetails } from '../../types/api.types';
import { API_URL } from '../api';

@Service()
export class MovieService {
  private readonly http = inject(HttpClient);

  public async get(movieId: string): Promise<MovieDetails | null> {
    try {
      return await firstValueFrom(this.http.get<MovieDetails>(this.url(movieId)));
    } catch (error) {
      if (error instanceof HttpErrorResponse && error.status === HttpStatusCode.NotFound) return null;
      throw error;
    }
  }

  public cities(movieId: string): Promise<City[]> {
    return firstValueFrom(this.http.get<City[]>(`${this.url(movieId)}/cities`));
  }

  public screeningDates(movieId: string, cityId: string): Promise<string[]> {
    return firstValueFrom(
      this.http.get<string[]>(`${this.url(movieId)}/screening-dates`, {
        params: { city_id: cityId },
      }),
    );
  }

  public screenings(movieId: string, cityId: string, date: string): Promise<CinemaScreenings[]> {
    return firstValueFrom(
      this.http.get<CinemaScreenings[]>(`${this.url(movieId)}/screenings`, {
        params: { city_id: cityId, date },
      }),
    );
  }

  private url(movieId: string): string {
    return `${API_URL}/movies/${encodeURIComponent(movieId)}`;
  }
}
