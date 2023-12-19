FROM python:3.9.13-slim
USER root

WORKDIR /workspace/src
COPY requirements.txt /workspace
RUN pip install -r /workspace/requirements.txt
COPY src/ .
# srcファイルをコピー
# 現段階のファイル構成は以下
# workspace
# ├─ requirements.txt
# └─ src
#     └─ ...

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
EXPOSE $PORT

CMD exec uvicorn --port $PORT --host 0.0.0.0 main:app