import { TestBed } from '@angular/core/testing';

import { TimepickingService } from './timepicking.service';

describe('TimepickingService', () => {
  let service: TimepickingService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TimepickingService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
