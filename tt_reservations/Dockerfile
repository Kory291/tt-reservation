FROM python:3.12

COPY . tt_reservations/
WORKDIR tt_reservations/

RUN pip install poetry
RUN poetry install
RUN apt-get update -y
RUN playwright install
# RUN apt-get install -y libX11-xcb.so.1 libXrandr.so.2 libXcomposite.so.1 libXcursor.so.1 libXdamage.so.1 libXfixes.so.3 libXi.so.6 libgtk-3.so.0 libgdk-3.so.0 libatk-1.0.so.0 libasound.so.2 libdbus-1.so.3

CMD ["fastapi", "run", "tt_reservations/main.py"]