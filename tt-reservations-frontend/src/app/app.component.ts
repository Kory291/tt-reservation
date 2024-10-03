import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { TimePickerComponent } from './time-picker/time-picker.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, TimePickerComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'tt-reservations-frontend';
}
