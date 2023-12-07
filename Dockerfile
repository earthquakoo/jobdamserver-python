FROM python:3.11

WORKDIR /jobdamserver

COPY ./requirements.txt /jobdamserver/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /jobdamserver/requirements.txt

COPY ./src /jobdamserver/src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
