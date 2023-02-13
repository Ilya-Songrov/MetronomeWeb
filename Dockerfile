FROM python:3.10.6-slim as builder
ENV PYTHONUNBUFFERED=1
ENV PIP_ROOT_USER_ACTION=ignore

RUN apt-get update && apt-get install -y gcc git build-essential
RUN pip install --upgrade pip setuptools wheel

WORKDIR /wheels
COPY requirements.txt /
RUN pip wheel -r /requirements.txt


FROM python:3.10.6-slim
ENV PYTHONUNBUFFERED=1
ENV PIP_ROOT_USER_ACTION=ignore

COPY --from=builder /wheels /wheels
RUN apt update && apt install -y gettext
RUN pip install --upgrade pip
RUN pip install /wheels/* \
        && rm -rf /wheels \
        && rm -rf /root/.cache/pip/*

WORKDIR /code
COPY . .

ENV METRONOME_SERVER_HOST=127.0.0.1
ENV METRONOME_SERVER_PORT=8080
ENV LOG_DIR_TO_SAVE='./Logs'

ENTRYPOINT ["/bin/bash", "-c"]
CMD ["python main.py --listen_host $METRONOME_SERVER_HOST --listen_port $METRONOME_SERVER_PORT --log_dir_to_save $LOG_DIR_TO_SAVE"]
