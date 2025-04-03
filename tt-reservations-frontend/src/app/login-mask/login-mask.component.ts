import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import {
  HttpClient,
  HttpContext,
  HttpHeaders,
  HttpParams,
} from '@angular/common/http';

@Component({
  selector: 'app-login-mask',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './login-mask.component.html',
  providers: [],
})
export class LoginMaskComponent implements OnInit {
  login_form: FormGroup = new FormGroup({});

  ngOnInit(): void {
    this.login_form = new FormGroup({
      username: new FormControl(''),
      password: new FormControl(''),
    });
  }

  constructor(private http: HttpClient) {}

  onSubmit() {
    if (!this.login_form.valid) {
      console.warn('Invalid login form');
      return;
    }
    const api_endpoint = 'http://localhost:8000/token';
    // const api_endpoint = 'https://lukas-schaefer.me/api/token';
    const http_params = new HttpParams()
      .set('username', this.login_form.value.username)
      .set('password', this.login_form.value.password);
    const headers: HttpHeaders = new HttpHeaders()
      .set('Access-Control-Allow-Origin', '*')
      .set('Content-Type', 'application/x-www-form-urlencoded')
      .set('Accept', 'application/json');
    this.http
      .post<{ access_token: string; token_type: string }>(
        api_endpoint,
        http_params.toString(),
        {
          headers: headers,
          observe: 'response',
        },
      )
      .subscribe((response) => {
        if (response.status !== 200) {
          console.error('Login failed');
          return;
        }
        if (!response.body || !response.body.access_token) {
          console.error('Access token is missing in the response');
          return;
        }
        const access_token: string = response.body.access_token;
      });
  }
}
