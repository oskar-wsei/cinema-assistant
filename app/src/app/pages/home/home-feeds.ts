import { Service, inject, resource } from '@angular/core';

import { FeedService } from '../../common/feed/feed.service';

@Service()
export class HomeFeeds {
  private readonly feedService = inject(FeedService);

  private readonly feeds = resource({ loader: () => this.feedService.list() });

  private readonly feedTitles: Record<string, string> = {
    'now-playing': 'Na ekranie',
    'coming-soon': 'Wkrótce',
    'watch-in-format': 'Oglądaj w formatach',
    'family-friendly': 'Dla całej rodziny',
    events: 'Wydarzenia',
  };

  public readonly sections = resource({
    params: ({ chain }) => chain(this.feeds),
    loader: ({ params: feeds }) =>
      Promise.all(
        feeds
          .filter((feed) => 'home' in feed.placements)
          .sort((a, b) => a.placements['home'] - b.placements['home'])
          .map(async (feed) => ({
            feedName: feed.name,
            title: this.feedTitle(feed.name),
            movies: await this.feedService.movies(feed.name),
          })),
      ),
  });

  public retry(): void {
    if (this.feeds.error()) this.feeds.reload();
    else this.sections.reload();
  }

  private feedTitle(feedName: string): string {
    const fallback = feedName.replaceAll('-', ' ');
    return this.feedTitles[feedName] ?? fallback.charAt(0).toUpperCase() + fallback.slice(1);
  }
}
