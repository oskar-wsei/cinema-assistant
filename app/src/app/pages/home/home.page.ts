import { Component, inject } from '@angular/core';

import { HomeFeeds } from './home-feeds';
import { MovieCarousel } from '../../common/movie/movie-carousel/movie-carousel';

const SKELETON_SECTIONS = 2;
const SKELETON_CARDS = 8;

@Component({
  selector: 'app-home',
  imports: [MovieCarousel],
  templateUrl: 'home.page.html',
  styleUrl: 'home.page.scss',
})
export default class HomePage {
  private readonly homeFeeds = inject(HomeFeeds);

  protected readonly sections = this.homeFeeds.sections;
  protected readonly skeletonSections = Array.from({ length: SKELETON_SECTIONS }, (_, i) => i);
  protected readonly skeletonCards = Array.from({ length: SKELETON_CARDS }, (_, i) => i);
}
