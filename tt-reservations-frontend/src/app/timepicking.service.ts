import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class TimepickingService {

  constructor(private http: HttpClient) { }

  get_available_timeslots(): Array<string> {
    let available_timeslots = Array<string>();
    // const api_endpoint = 'https://tt-reservation.lukas-schaefer.me/api/available_timeslots';
    const api_endpoint = 'http://localhost:8000/available_timeslots';
    this.http.get<{available_timeslots: Array<string>}>(api_endpoint).subscribe((response) => {
      console.info('Available timeslots:', response.available_timeslots);
      let available_timeslots = response.available_timeslots;
    });
    return available_timeslots;
  }

  get_suggested_date(): string {
    let current_date = new Date();
    console.log("current_date: " + current_date);
    let available_timeslots = this.get_available_timeslots();
    console.log("available_timeslots (from get_suggested_date): " + available_timeslots);
    return "2024-06-07"; // Placeholder date
  }
}
