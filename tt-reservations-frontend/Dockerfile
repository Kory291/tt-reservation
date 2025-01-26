FROM node:20.17.0-alpine

COPY tt-reservations-frontend /usr/src/app
WORKDIR /usr/src/app

ENV SSL_CERT = ""
ENV SSL_KEY = ""

RUN npm install -g @angular/cli
RUN npm install

ENTRYPOINT ["sh", "entrypoint.sh"]