import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LoginMaskComponent } from './login-mask.component';

describe('LoginMaskComponent', () => {
  let component: LoginMaskComponent;
  let fixture: ComponentFixture<LoginMaskComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LoginMaskComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(LoginMaskComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
