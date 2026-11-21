import { Component, computed, input, output } from '@angular/core';
import { DatePipe } from '@angular/common';

import { addDays, localIsoDate } from '../../date.utils';

@Component({
  selector: 'app-day-picker',
  imports: [DatePipe],
  templateUrl: 'day-picker.html',
  styleUrl: 'day-picker.scss',
})
export class DayPicker {
  public readonly days = input.required<string[]>();
  public readonly selected = input.required<string>();
  public readonly selectedChange = output<string>();

  protected readonly options = computed(() => {
    const today = new Date();
    const relativeNames = new Map([
      [localIsoDate(today), 'Dziś'],
      [localIsoDate(addDays(today, 1)), 'Jutro'],
    ]);
    return this.days().map((day) => ({ day, relativeName: relativeNames.get(day) }));
  });
}
