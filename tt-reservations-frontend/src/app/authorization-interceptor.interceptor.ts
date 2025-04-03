import {
  HttpHandler,
  HttpInterceptorFn,
  HttpRequest,
  HttpHandlerFn,
} from '@angular/common/http';
import { inject } from '@angular/core';
import { AccessTokenHandlerService } from './access-token-handler.service';

export const authorizationInterceptor: HttpInterceptorFn = (
  req: HttpRequest<unknown>,
  next: HttpHandlerFn,
) => {
  const accessTokenHandlerService = inject(AccessTokenHandlerService);
  const accessToken = accessTokenHandlerService.getAccessToken();
  if (accessToken) {
    req = req.clone({
      setHeaders: {
        Authorization: `Bearer ${accessToken}`,
      },
    });
  } else {
    console.warn('No access token found, skipping authorization header');
  }
  return next(req);
};
