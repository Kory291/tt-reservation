FROM ubuntu:noble

RUN apt-get update -y
RUN apt-get install -y python3 python3-pip python3-venv

COPY . tt_reservations/
WORKDIR tt_reservations/
EXPOSE 8000

RUN python3 -m venv venv 
RUN venv/bin/pip install poetry
RUN . venv/bin/activate && poetry lock && poetry install && playwright install && playwright install-deps

CMD ["venv/bin/fastapi", "run", "tt_reservations/main.py"]