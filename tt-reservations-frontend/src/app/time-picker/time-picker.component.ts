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
    return "2024-06-07"
  }

  get_suggested_start_time() {
    return "19:00"
  }

  get_suggested_end_time() {
    return "22:00"
  }


  async book_time(start_day: string, start_time: string, end_time: string) {
    const headers: Headers = new Headers();
    headers.set("Access-Control-Allow-Origin", "*")
    headers.set("Accept", "application/json")
    const request: RequestInfo = new Request("http://lukas-schaefer.me:9000/reserve_time?start_time="+start_day+"T"+encodeURIComponent(start_time)+"&end_time="+start_day+"T"+encodeURIComponent(end_time), {method: 'POST', headers: headers});
    return await fetch(request);
  }

  onSubmit() {
    if (this.chosen_time.valid) {
      console.warn(this.chosen_time.value);
      var start_day = this.chosen_time.value.day;
      var start_time = this.chosen_time.value.start_time;
      var end_time = this.chosen_time.value.end_time;
      var result = this.book_time(start_day, start_time, end_time);
      console.log(result);
      alert("Submitted booking with" + this.chosen_time.value + " !");

    } else {
      console.error("Form is invalid");
    }
  }
}
