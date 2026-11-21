import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    title: 'Cinema City',
    loadComponent: () => import('./pages/home/home.page'),
  },
  {
    path: 'movies/:movieId',
    loadComponent: () => import('./pages/movie/movie.page'),
  },
];
