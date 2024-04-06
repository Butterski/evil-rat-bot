FROM python:3.10

RUN useradd --create-home rat-user
USER rat-user

WORKDIR /bot

COPY . /bot

COPY run.sh /run.sh
RUN chmod +x /run.sh
CMD ["/run.sh"]

ENTRYPOINT ["python3", "main.py"]
