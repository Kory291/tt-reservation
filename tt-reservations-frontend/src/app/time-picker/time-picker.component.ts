import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { ReactiveFormsModule  } from '@angular/forms';

@Component({
  selector: 'app-time-picker',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './time-picker.component.html',
  styleUrl: './time-picker.component.scss'
})
export class TimePickerComponent implements OnInit {
  chosen_time: FormGroup = new FormGroup({});
  
  ngOnInit(): void {
    this.chosen_time = new FormGroup({
      day: new FormControl(this.get_suggested_date()),
      start_time: new FormControl(this.get_suggested_start_time()),
      end_time: new FormControl(this.get_suggested_end_time())
    });    
  }

  get_suggested_date() {
    return "2024-09-15"
  }

  get_suggested_start_time() {
    return ""
  }

  get_suggested_end_time() {
    return ""
  }

  onSubmit() {
    if (this.chosen_time.valid) {
      console.warn(this.chosen_time.value);
    } else {
      console.error("Form is invalid");
    }
  }
}
