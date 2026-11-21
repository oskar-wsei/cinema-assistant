import { HttpClient } from '@angular/common/http';
import { Service, inject } from '@angular/core';
import { firstValueFrom } from 'rxjs';

import { Feed, Movie } from '../../types/api.types';
import { API_URL } from '../api';

@Service()
export class FeedService {
  private readonly http = inject(HttpClient);

  public list(): Promise<Feed[]> {
    return firstValueFrom(this.http.get<Feed[]>(`${API_URL}/feeds`));
  }

  public movies(feedName: string): Promise<Movie[]> {
    return firstValueFrom(
      this.http.get<Movie[]>(`${API_URL}/feeds/${encodeURIComponent(feedName)}/movies`),
    );
  }
}
