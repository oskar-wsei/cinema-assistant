import { Service, signal } from '@angular/core';

const STORAGE_KEY = 'cinemacity.cityId';
const DEFAULT_CITY_ID = 'krakow';

/** The city the user last chose, remembered across visits. */
@Service()
export class CityPreference {
  private readonly preferredCityId = signal(this.readStoredCityId() ?? DEFAULT_CITY_ID);

  public readonly cityId = this.preferredCityId.asReadonly();

  public set(cityId: string): void {
    this.preferredCityId.set(cityId);
    try {
      localStorage.setItem(STORAGE_KEY, cityId);
    } catch {}
  }

  private readStoredCityId(): string | null {
    try {
      return localStorage.getItem(STORAGE_KEY);
    } catch {
      return null;
    }
  }
}
