import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-time-picker',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './time-picker.component.html',
  styleUrl: './time-picker.component.scss',
})
export class TimePickerComponent implements OnInit {
  chosen_time: FormGroup = new FormGroup({});

  ngOnInit(): void {
    this.chosen_time = new FormGroup({
      day: new FormControl(this.get_suggested_date()),
      start_time: new FormControl(this.get_suggested_start_time()),
      end_time: new FormControl(this.get_suggested_end_time()),
    });
  }

  constructor(private http: HttpClient) {}

  get_suggested_date() {
    return '2024-06-07';
  }

  get_suggested_start_time() {
    return '19:00';
  }

  get_suggested_end_time() {
    return '22:00';
  }

  async book_time(start_day: string, start_time: string, end_time: string) {
    const headers: HttpHeaders = new HttpHeaders()
      .set('Access-Control-Allow-Origin', '*')
      .set('Accept', 'application/json')
      .set('Content-Type', 'application/x-www-form-urlencoded');
    const api_endpoint =
      'https://tt-reservation.lukas-schaefer.me/api/reserve_time?start_time=' +
      start_day +
      'T' +
      encodeURIComponent(start_time) +
      '&end_time=' +
      start_day +
      'T' +
      encodeURIComponent(end_time);
    // const api_endpoint = 'http://localhost:8000/reserve_time?start_time=' + start_day + 'T' + encodeURIComponent(start_time) + '&end_time=' + start_day + 'T' + encodeURIComponent(end_time);
    this.http.post(api_endpoint, { headers: headers }).subscribe({
      next: (response) => {
        console.info('Booking successful:', response);
      },
      error: () => {
        console.error('Booking failed');
      },
      complete: () => {
        console.info('Booking request completed');
      },
    });
  }

  onSubmit() {
    if (this.chosen_time.valid) {
      console.info(this.chosen_time.value);
      let start_day = this.chosen_time.value.day;
      let start_time = this.chosen_time.value.start_time;
      let end_time = this.chosen_time.value.end_time;
      this.book_time(start_day, start_time, end_time);
      alert('Submitted booking with' + this.chosen_time.value + ' !');
    } else {
      console.error('Form is invalid');
    }
  }
}
