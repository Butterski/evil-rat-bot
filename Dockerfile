FROM python:3.10

RUN useradd --create-home rat-user
USER rat-user

WORKDIR /bot

COPY . /bot

RUN run.sh

ENTRYPOINT ["python3", "main.py"]
