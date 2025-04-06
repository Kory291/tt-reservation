import { Injectable } from '@angular/core';
import {
  HttpClient,
  HttpContext,
  HttpHeaders,
  HttpParams,
} from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class AccessTokenHandlerService {
  constructor(private http: HttpClient) {}

  setAccessToken(token: string) {
    localStorage.setItem('access_token', token);
  }
  getAccessToken(): string | null {
    return localStorage.getItem('access_token');
  }
  removeAccessToken() {
    localStorage.removeItem('access_token');
  }

  retrieveAccessToken(username: string, password: string): void {
    const api_endpoint = 'http://localhost:8000/token';
    // const api_endpoint = 'https://tt-reservation.lukas-schaefer.me/api/token';
    const http_params = new HttpParams()
      .set('username', username)
      .set('password', password);
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
        if (!access_token) {
          console.error('Access token is null or undefined');
          return;
        }
        this.setAccessToken(access_token);
        console.info('Access token retrieved:', access_token);
      });
  }
}
