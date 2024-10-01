import { Component } from '@angular/core';
import { FormControl } from '@angular/forms';

@Component({
  selector: 'app-time-picker',
  standalone: true,
  imports: [],
  templateUrl: './time-picker.component.html',
  styleUrl: './time-picker.component.scss'
})
export class TimePickerComponent {
  day = new FormControl('');
}
