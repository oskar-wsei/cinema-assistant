import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

import { ChatWidget } from './layout/chat-widget/chat-widget';
import { Header } from './layout/header/header';

@Component({
  imports: [RouterOutlet, ChatWidget, Header],
  selector: 'app-root',
  styleUrl: 'app.scss',
  templateUrl: 'app.html',
})
export class App {}
