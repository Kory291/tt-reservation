import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { ReactiveFormsModule  } from '@angular/forms';
import { HttpClient, HttpContext, HttpHeaders, HttpParams } from '@angular/common/http';

@Component({
  selector: 'app-login-mask',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './login-mask.component.html',
  providers: []
})
export class LoginMaskComponent implements OnInit {
  login_form: FormGroup = new FormGroup({});

  ngOnInit(): void {
    this.login_form = new FormGroup({username: new FormControl(''), password: new FormControl('')});
  }
  
  constructor(private http: HttpClient) {  }

  onSubmit() {
    if (!this.login_form.valid) {
      console.warn('Invalid login form');
      return;
    }
    const api_endpoint = 'http://localhost:8000/token'
    // const api_endpoint = 'https://lukas-schaefer.me/api/token';
    const http_params = new HttpParams().set('username', this.login_form.value.username).set('password', this.login_form.value.password);
    this.http.post(api_endpoint, http_params.toString(), {headers: new HttpHeaders().set('Content-Type', 'application/x-www-form-urlencoded'), observe: 'response'}).subscribe(response => {
      if (response.status !== 200) {
        console.error('Login failed');
        return;
      }
      // let accessToken = response.body['access_token'];
      // console.log('Access token:', accessToken);
      // console.log(response.body.access_token);
      if (response.body === null) {
        console.error('Response body is null');
        return;
      }
      console.log(response.body['token_type']);
    });
  }
}

