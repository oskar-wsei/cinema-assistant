import { Languages } from '../../types/api.types';

/** Screening formats, in display order. */
const FORMAT_LABELS = {
  imax: 'IMAX',
  '4dx': '4DX',
  screenx: 'ScreenX',
  vip: 'VIP',
  '3d': '3D',
  '2d': '2D',
} as const;

export type FormatId = keyof typeof FORMAT_LABELS;

const ALL_FORMATS = Object.keys(FORMAT_LABELS) as FormatId[];

/** Premium formats worth highlighting on movie posters. */
export const HIGHLIGHTED_FORMATS: readonly FormatId[] = ['imax', '4dx', 'screenx', '3d'];

const EXTRA_LABELS: Record<string, string> = {
  'laser-barco': 'Projekcja laserowa Barco',
  'dolby-atmos': 'Dolby Atmos',
  hfr: 'HFR',
  recliners: 'Fotele rozkładane',
};

const GENRE_LABELS: Record<string, string> = {
  action: 'akcja',
  'action-packed': 'akcja',
  'adult-animation': 'animacja dla dorosłych',
  adventure: 'przygodowy',
  'adventure-fantasy': 'przygodowy',
  animation: 'animacja',
  biography: 'biograficzny',
  'black-comedy': 'czarna komedia',
  catastrophic: 'katastroficzny',
  comedy: 'komedia',
  'comedy-drama': 'komediodramat',
  'concert-live': 'koncert',
  'concert-movie': 'koncert',
  'concert-rebroadcast': 'koncert',
  'costume-drama': 'kostiumowy',
  crime: 'kryminał',
  documentary: 'dokumentalny',
  drama: 'dramat',
  family: 'familijny',
  history: 'historyczny',
  holiday: 'świąteczny',
  'music-event': 'wydarzenie muzyczne',
  'nature-documentary': 'przyrodniczy',
  psychological: 'psychologiczny',
  romance: 'romans',
  'romantic-comedy': 'komedia romantyczna',
  sport: 'sportowy',
  'true-crime': 'true crime',
  war: 'wojenny',
};

const languageNames = new Intl.DisplayNames(['pl'], { type: 'language' });

/** Labels of the formats among `attributes`, e.g. `['IMAX', '2D']`. */
export function formatLabels(
  attributes: readonly string[],
  formats: readonly FormatId[] = ALL_FORMATS,
): string[] {
  const present = new Set(attributes);
  return formats.filter((format) => present.has(format)).map((format) => FORMAT_LABELS[format]);
}

/** Labels of projection and comfort extras among `attributes`. */
export function extraLabels(attributes: readonly string[]): string[] {
  return attributes.flatMap((attribute) => EXTRA_LABELS[attribute] ?? []);
}

export function genreLabel(genre: string): string {
  return GENRE_LABELS[genre] ?? genre.replaceAll('-', ' ');
}

/** Polish name of an ISO 639-1 language code, e.g. `en` → `angielski`. */
export function languageName(code: string): string {
  try {
    return languageNames.of(code) ?? code;
  } catch {
    return code;
  }
}

/** Language version of a screening, e.g. `Angielski (napisy: polski)`. */
export function languageVersionLabel(languages: Languages): string {
  const original = languages.original.map(languageName).join(', ');
  const translation = translationLabel(languages);
  const label =
    original && translation
      ? `${original} (${translation})`
      : original || translation || 'wersja oryginalna';
  return label.charAt(0).toUpperCase() + label.slice(1);
}

function translationLabel({ dubbed, voiceover, subtitles }: Languages): string {
  const [kind, codes] = dubbed.length
    ? ['dubbing', dubbed]
    : voiceover.length
      ? ['lektor', voiceover]
      : ['napisy', subtitles];
  return codes.length ? `${kind}: ${codes.map(languageName).join(', ')}` : '';
}

/** Age rating label, e.g. `Od 15 lat`, or `null` when unknown. */
export function ageRatingLabel(code: string): string | null {
  if (code === 'bez-ograniczen') return 'Bez ograniczeń';
  const minimumAge = /^(\d+)-plus$/.exec(code)?.[1];
  return minimumAge ? `Od ${minimumAge} lat` : null;
}

/** Duration such as `2 godz. 38 min`. */
export function durationLabel(minutes: number): string {
  const hours = Math.floor(minutes / 60);
  const rest = minutes % 60;
  return [hours && `${hours} godz.`, rest && `${rest} min`].filter(Boolean).join(' ');
}
