FROM python:3.10

RUN useradd --create-home rat-user
USER rat-user

WORKDIR /bot

COPY . /bot
COPY requirements.txt /bot/requirements.txt

RUN pip install --no-warn-script-location -r requirements.txt


ENTRYPOINT ["python3", "main.py"]
