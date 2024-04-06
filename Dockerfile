FROM python:3.10

RUN useradd --create-home rat-user
USER rat-user

WORKDIR /bot

COPY . /bot
RUN ./run.sh

RUN pip install --no-warn-script-location -r requirements.txt


ENTRYPOINT ["python3", "main.py"]
