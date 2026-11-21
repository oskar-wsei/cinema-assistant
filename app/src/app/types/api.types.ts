/* eslint-disable */
/* tslint:disable */
// @ts-nocheck
/*
 * ---------------------------------------------------------------
 * ## THIS FILE WAS GENERATED VIA SWAGGER-TYPESCRIPT-API        ##
 * ##                                                           ##
 * ## AUTHOR: acacode                                           ##
 * ## SOURCE: https://github.com/acacode/swagger-typescript-api ##
 * ---------------------------------------------------------------
 */

/** MovieStatus */
export type MovieStatus = "showing" | "upcoming" | "past";

/** Address */
export interface Address {
  /** Street */
  street: string;
  /** Postal Code */
  postal_code: string;
  /** City */
  city: string;
}

/** AgeRating */
export interface AgeRating {
  /** Code */
  code: string;
  /** Icon Url */
  icon_url: string;
}

/** Attribute */
export interface Attribute {
  /**
   * Id
   * Value for the `attribute` query parameter.
   */
  id: string;
  /** Icon Url */
  icon_url: string | null;
  /**
   * Visible
   * Whether the website shows it as a filter.
   */
  visible: boolean;
}

/** AttributeGroup */
export interface AttributeGroup {
  /** Name */
  name: string;
  /** Attributes */
  attributes: Attribute[];
}

/** Cinema */
export interface Cinema {
  /** Id */
  id: string;
  /** Name */
  name: string;
  /** City Id */
  city_id: string;
  address: Address;
  coordinates: Coordinates;
  /** Image Url */
  image_url: string;
  /**
   * Website Url
   * Cinema page on the Cinema City website.
   */
  website_url: string;
}

/**
 * CinemaScreenings
 * A cinema together with its screenings of the requested movie.
 */
export interface CinemaScreenings {
  cinema: Cinema;
  /** Screenings */
  screenings: Screening[];
}

/** City */
export interface City {
  /** Id */
  id: string;
  /** Name */
  name: string;
  /** Cinema Ids */
  cinema_ids: string[];
}

/** Conversation */
export interface Conversation {
  /**
   * Id
   * The unique identifier of the conversation.
   */
  id: string;
  /**
   * Created At
   * The creation timestamp of the conversation.
   * @format date-time
   */
  created_at: string;
}

/** Coordinates */
export interface Coordinates {
  /** Latitude */
  latitude: number;
  /** Longitude */
  longitude: number;
}

/** ErrorResponse */
export interface ErrorResponse {
  /**
   * Detail
   * Human-readable error description.
   */
  detail: string;
}

/** Feed */
export interface Feed {
  /** Name */
  name: string;
  /**
   * Placements
   * Website page name mapped to the position of the feed on it.
   */
  placements: Record<string, number>;
}

/** HTTPValidationError */
export interface HTTPValidationError {
  /** Detail */
  detail?: ValidationError[];
}

/** HealthStatus */
export interface HealthStatus {
  /** Status */
  status: "ok";
}

/** Languages */
export interface Languages {
  /**
   * Original
   * Original languages.
   */
  original: string[];
  /**
   * Dubbed
   * Dubbing languages.
   */
  dubbed: string[];
  /**
   * Voiceover
   * Voice-over languages.
   */
  voiceover: string[];
  /**
   * Subtitles
   * Subtitle languages.
   */
  subtitles: string[];
}

/** Message */
export interface Message {
  /**
   * Id
   * The unique identifier of the message.
   */
  id: string;
  /**
   * Role
   * The role of the message sender.
   */
  role: string;
  /**
   * Content
   * The content of the message.
   */
  content: string;
  /**
   * Created At
   * The creation timestamp of the message.
   * @format date-time
   */
  created_at: string;
}

/** MessageCreate */
export interface MessageCreate {
  /**
   * Content
   * The content of the message.
   * @minLength 1
   * @maxLength 2000
   */
  content: string;
}

/** Movie */
export interface Movie {
  /** Id */
  id: string;
  /** Title */
  title: string;
  /** Poster Url */
  poster_url: string;
  /** Trailer Url */
  trailer_url: string | null;
  /**
   * Website Url
   * Movie page on the Cinema City website.
   */
  website_url: string;
  /** Release Date */
  release_date: string | null;
  /**
   * Duration Minutes
   * Not available in movie listings, only for bookable movies.
   */
  duration_minutes: number | null;
  /**
   * Attributes
   * Genres, formats and language versions, e.g. `action`, `4dx`.
   */
  attributes: string[];
  languages: Languages;
}

/** MovieDetails */
export interface MovieDetails {
  /** Id */
  id: string;
  /** Title */
  title: string;
  /** Poster Url */
  poster_url: string;
  /** Trailer Url */
  trailer_url: string | null;
  /**
   * Website Url
   * Movie page on the Cinema City website.
   */
  website_url: string;
  /** Release Date */
  release_date: string | null;
  /**
   * Duration Minutes
   * Not available in movie listings, only for bookable movies.
   */
  duration_minutes: number | null;
  /**
   * Attributes
   * Genres, formats and language versions, e.g. `action`, `4dx`.
   */
  attributes: string[];
  languages: Languages;
  /** Original Title */
  original_title: string;
  status: MovieStatus;
  /** Synopsis */
  synopsis: string;
  /** Cast */
  cast: string[];
  /** Directors */
  directors: string[];
  /** Release Year */
  release_year: number | null;
  /** Release Country */
  release_country: string | null;
  /** Genres */
  genres: string[];
  age_rating: AgeRating;
  /**
   * Screening Count
   * Number of scheduled screenings.
   */
  screening_count: number;
}

/**
 * MovieScreenings
 * A movie together with its screenings in the requested cinema.
 */
export interface MovieScreenings {
  movie: Movie;
  /** Screenings */
  screenings: Screening[];
}

/**
 * PresaleMovie
 * A not yet released movie with screenings already open for booking.
 */
export interface PresaleMovie {
  movie: Movie;
  /** Screening Dates */
  screening_dates: string[];
}

/** Screening */
export interface Screening {
  /** Id */
  id: string;
  /** Movie Id */
  movie_id: string;
  /** Cinema Id */
  cinema_id: string;
  /**
   * Starts At
   * Start time in the cinema's local time.
   * @format date-time
   */
  starts_at: string;
  /**
   * Business Date
   * Cinema business day; late-night screenings belong to the previous day.
   * @format date
   */
  business_date: string;
  /** Auditorium */
  auditorium: string;
  /** Attributes */
  attributes: string[];
  languages: Languages;
  /**
   * Seat Availability
   * Fraction of seats still available.
   * @min 0
   * @max 1
   */
  seat_availability: number;
  /** Sold Out */
  sold_out: boolean;
  /** Booking Url */
  booking_url: string;
}

/** Trailer */
export interface Trailer {
  /** Movie Id */
  movie_id: string;
  /** Movie Title */
  movie_title: string;
  /**
   * Movie Url
   * Movie page on the Cinema City website.
   */
  movie_url: string;
  /** Video Url */
  video_url: string | null;
}

/** ValidationError */
export interface ValidationError {
  /** Location */
  loc: (string | number)[];
  /** Message */
  msg: string;
  /** Error Type */
  type: string;
  /** Input */
  input?: any;
  /** Context */
  ctx?: object;
}

export interface ListMoviesMoviesGetParams {
  /**
   * Status
   * Only movies with this status. Omit to list all movies.
   */
  status?: MovieStatus | null;
  /**
   * Cinema Id
   * Only movies screened in this cinema.
   */
  cinema_id?: string | null;
  /**
   * Attribute
   * Only include results with this attribute, e.g. a format (`4dx`, `imax`) or language version (`dubbed`). Repeatable. See `GET /attributes`.
   */
  attribute?: string[] | null;
}

export interface ListBookableMoviesMoviesBookableGetParams {
  /**
   * Until
   * Last day to include. Defaults to a year from today.
   */
  until?: string | null;
  /**
   * Attribute
   * Only include results with this attribute, e.g. a format (`4dx`, `imax`) or language version (`dubbed`). Repeatable. See `GET /attributes`.
   */
  attribute?: string[] | null;
}

export interface GetMovieMoviesMovieIdGetParams {
  /**
   * Movie Id
   * Movie id, see `GET /movies`.
   */
  movieId: string;
}

export interface ListMovieCitiesMoviesMovieIdCitiesGetParams {
  /**
   * Until
   * Last day to include. Defaults to a year from today.
   */
  until?: string | null;
  /**
   * Attribute
   * Only include results with this attribute, e.g. a format (`4dx`, `imax`) or language version (`dubbed`). Repeatable. See `GET /attributes`.
   */
  attribute?: string[] | null;
  /**
   * Movie Id
   * Movie id, see `GET /movies`.
   */
  movieId: string;
}

export interface ListMovieScreeningDatesMoviesMovieIdScreeningDatesGetParams {
  /**
   * Until
   * Last day to include. Defaults to a year from today.
   */
  until?: string | null;
  /**
   * Attribute
   * Only include results with this attribute, e.g. a format (`4dx`, `imax`) or language version (`dubbed`). Repeatable. See `GET /attributes`.
   */
  attribute?: string[] | null;
  /**
   * City Id
   * Search in all cinemas of this city.
   */
  city_id?: string | null;
  /**
   * Cinema Id
   * Search in this cinema. Repeatable.
   */
  cinema_id?: string[] | null;
  /**
   * Movie Id
   * Movie id, see `GET /movies`.
   */
  movieId: string;
}

export interface ListMovieScreeningsMoviesMovieIdScreeningsGetParams {
  /**
   * Date
   * Day of the screenings. Defaults to today.
   */
  date?: string | null;
  /**
   * Attribute
   * Only include results with this attribute, e.g. a format (`4dx`, `imax`) or language version (`dubbed`). Repeatable. See `GET /attributes`.
   */
  attribute?: string[] | null;
  /**
   * City Id
   * Search in all cinemas of this city.
   */
  city_id?: string | null;
  /**
   * Cinema Id
   * Search in this cinema. Repeatable.
   */
  cinema_id?: string[] | null;
  /**
   * Movie Id
   * Movie id, see `GET /movies`.
   */
  movieId: string;
}

export interface ListCinemasCinemasGetParams {
  /**
   * Attribute
   * Only include results with this attribute, e.g. a format (`4dx`, `imax`) or language version (`dubbed`). Repeatable. See `GET /attributes`.
   */
  attribute?: string[] | null;
}

export interface GetCinemaCinemasCinemaIdGetParams {
  /**
   * Cinema Id
   * Cinema id, see `GET /cinemas`.
   */
  cinemaId: string;
}

export interface ListCinemaTrailersCinemasCinemaIdTrailersGetParams {
  /**
   * Cinema Id
   * Cinema id, see `GET /cinemas`.
   */
  cinemaId: string;
}

export interface ListCinemaScreeningDatesCinemasCinemaIdScreeningDatesGetParams {
  /**
   * Until
   * Last day to include. Defaults to a year from today.
   */
  until?: string | null;
  /**
   * Attribute
   * Only include results with this attribute, e.g. a format (`4dx`, `imax`) or language version (`dubbed`). Repeatable. See `GET /attributes`.
   */
  attribute?: string[] | null;
  /**
   * Cinema Id
   * Cinema id, see `GET /cinemas`.
   */
  cinemaId: string;
}

export interface ListCinemaScreeningsCinemasCinemaIdScreeningsGetParams {
  /**
   * Date
   * Day of the screenings. Defaults to today.
   */
  date?: string | null;
  /**
   * Attribute
   * Only include results with this attribute, e.g. a format (`4dx`, `imax`) or language version (`dubbed`). Repeatable. See `GET /attributes`.
   */
  attribute?: string[] | null;
  /**
   * Cinema Id
   * Cinema id, see `GET /cinemas`.
   */
  cinemaId: string;
}

export interface ListCinemaPresalesCinemasCinemaIdPresalesGetParams {
  /**
   * As Of
   * Reference day for "not yet released". Defaults to today.
   */
  as_of?: string | null;
  /**
   * Attribute
   * Only include results with this attribute, e.g. a format (`4dx`, `imax`) or language version (`dubbed`). Repeatable. See `GET /attributes`.
   */
  attribute?: string[] | null;
  /**
   * Cinema Id
   * Cinema id, see `GET /cinemas`.
   */
  cinemaId: string;
}

export interface GetCityCitiesCityIdGetParams {
  /**
   * City Id
   * City id, see `GET /cities`.
   */
  cityId: string;
}

export interface ListCityCinemasCitiesCityIdCinemasGetParams {
  /**
   * City Id
   * City id, see `GET /cities`.
   */
  cityId: string;
}

export interface GetFeedFeedsFeedNameGetParams {
  /**
   * Feed Name
   * Feed name, see `GET /feeds`.
   */
  feedName: string;
}

export interface ListFeedMoviesFeedsFeedNameMoviesGetParams {
  /**
   * Feed Name
   * Feed name, see `GET /feeds`.
   */
  feedName: string;
}

export interface GetConversationChatConversationsConversationIdGetParams {
  /** Conversation Id */
  conversationId: string;
}

export interface ListMessagesChatConversationsConversationIdMessagesGetParams {
  /** Conversation Id */
  conversationId: string;
}

export interface CreateMessageChatConversationsConversationIdMessagesPostParams {
  /** Conversation Id */
  conversationId: string;
}
