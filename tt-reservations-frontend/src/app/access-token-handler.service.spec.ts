import { TestBed } from '@angular/core/testing';

import { AccessTokenHandlerService } from './access-token-handler.service';

describe('AccessTokenHandlerService', () => {
  let service: AccessTokenHandlerService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AccessTokenHandlerService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
