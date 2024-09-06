# TT reservation

This tool wraps the booking system of mytischtennis.de.
This should be done, because I don't want to always book training times three times for a day.


## Commands

Run these commands from the project root

### Docker thingies

- Build a new image:
  ```shell
  docker build -t tt_reservation -f tt_reservations/Dockerfile .
  ```

- Run an existing image:
    ```shell
    docker run -p 8000:8000 --rm --env-file .env tt_reservation
    ```