import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { TimePickerComponent } from './time-picker/time-picker.component';
import { LoginMaskComponent } from './login-mask/login-mask.component';
import { NgIf } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, TimePickerComponent, LoginMaskComponent, NgIf],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent {
  title = 'tt-reservations-frontend';
  logged_in: boolean = false;

  constructor() {

  }

  on_logged_in() {
    this.logged_in = true;
    console.log('User logged in');
  }
}
