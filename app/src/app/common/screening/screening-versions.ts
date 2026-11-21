import { Screening } from '../../types/api.types';
import { extraLabels, formatLabels, languageVersionLabel } from '../movie/movie-labels';

/** Screenings sharing the same format, language version and extras. */
export interface ScreeningVersion {
  key: string;
  formats: string[];
  language: string;
  extras: string[];
  screenings: Screening[];
}

/** Group screenings into versions, plain formats first, keeping screening order. */
export function groupByVersion(screenings: readonly Screening[]): ScreeningVersion[] {
  const versions = new Map<string, ScreeningVersion>();
  for (const screening of screenings) {
    const formats = formatLabels(screening.attributes);
    const language = languageVersionLabel(screening.languages);
    const extras = extraLabels(screening.attributes);
    const key = [...formats, language, ...extras].join('|');

    const version = versions.get(key) ?? { key, formats, language, extras, screenings: [] };
    version.screenings.push(screening);
    versions.set(key, version);
  }
  return [...versions.values()].sort(
    (a, b) => a.formats.length - b.formats.length || a.key.localeCompare(b.key, 'pl'),
  );
}
