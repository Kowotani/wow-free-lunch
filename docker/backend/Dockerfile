FROM python:3.8.16-alpine

# copy requirements
WORKDIR /app
COPY ../dj_wfl/requirements.txt /app/backend/dj_wfl/requirements.txt
COPY ../server/requirements.txt /app/backend/server/requirements.txt

# install pre-reqs
RUN apk add build-base
RUN apk add krb5-dev
RUN apk add libffi-dev
RUN apk add mariadb-connector-c-dev

# install requirements
RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install -r backend/dj_wfl/requirements.txt
RUN pip install -r backend/server/requirements.txt

# copy source code
COPY ./docker /app/docker
COPY ./dj_wfl /app/backend/dj_wfl
COPY ./server /app/backend/server