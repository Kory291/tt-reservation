import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import {
  HttpClient,
  HttpContext,
  HttpHeaders,
  HttpParams,
} from '@angular/common/http';
import { AccessTokenHandlerService } from '../access-token-handler.service';

@Component({
  selector: 'app-login-mask',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './login-mask.component.html',
  styleUrl: './login-mask.component.scss',
  providers: [],
})
export class LoginMaskComponent implements OnInit {
  login_form: FormGroup = new FormGroup({});

  @Output() login_event = new EventEmitter<void>();

  ngOnInit(): void {
    this.login_form = new FormGroup({
      username: new FormControl(''),
      password: new FormControl(''),
    });
  }

  constructor(
    private http: HttpClient,
    private access_token_handler_service: AccessTokenHandlerService,
  ) {}

  onSubmit() {
    if (!this.login_form.valid) {
      console.warn('Invalid login form');
      return;
    }
    this.access_token_handler_service.retrieveAccessToken(
      this.login_form.value.username,
      this.login_form.value.password,
    );
    this.login_form.reset();
    if (this.access_token_handler_service.getAccessToken()) {
      console.log('User logged in');
      this.login_event.emit();
    } else {
      console.error('User login failed');
    }
    
  }
}
