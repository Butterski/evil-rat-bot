FROM python:3.10

RUN useradd --create-home rat-user

WORKDIR /bot

COPY . /bot

COPY run.sh /run.sh
RUN chmod +x /run.sh

USER rat-user

RUN pip install -r requirements.txt

CMD ["/run.sh"]
ENTRYPOINT ["python3", "main.py"]