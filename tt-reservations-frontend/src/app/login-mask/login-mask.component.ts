import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { ReactiveFormsModule  } from '@angular/forms';

@Component({
  selector: 'app-login-mask',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './login-mask.component.html',
  styleUrl: './login-mask.component.scss'
})
export class LoginMaskComponent implements OnInit {
  login_form: FormGroup = new FormGroup({});

  ngOnInit(): void {
    this.login_form = new FormGroup({username: new FormControl(''), password: new FormControl('')});
  }
  
  onSubmit() {
    if (this.login_form.valid) {
      console.info(this.login_form.value.username);
    }
  }
}

