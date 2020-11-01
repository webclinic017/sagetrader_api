FROM node:12 as frontend
COPY . /app
WORKDIR /app
# RUN cd frontend/nuxt && yarn install && yarn build

FROM python:3.8-slim
WORKDIR /app
RUN groupadd --gid 10001 app && useradd -g app --uid 10001 --shell /usr/sbin/nologin app
RUN chown app:app /tmp
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    gcc apt-transport-https python-dev \
    build-essential libpq-dev
COPY ./backend/django/requirements.txt /app/backend/django/requirements.txt
RUN pip install --upgrade --no-cache-dir -r backend/django/requirements.txt

COPY . /app
COPY --from=frontend /app/frontend/nuxt/dist /app/frontend/nuxt/dist
# RUN chmod +x /app/backend/startup.sh
RUN python /app/backend/django/manage.py makemigrations &&\
    python /app/backend/django/manage.py migrate &&\
    python /app/backend/django/manage.py shell < /app/backend/django/init_admin.py

USER app

ENV PORT=8000
EXPOSE $PORT

CMD python backend/django/manage.py runserver 0.0.0.0:$PORT
#