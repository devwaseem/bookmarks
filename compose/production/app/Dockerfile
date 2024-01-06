FROM python:3.11.5-bullseye

ARG APP_HOME=/app
ARG BUILD_ENVIRONMENT=production
ARG UID=1000
ARG GID=1000

ENV DJANGO_ENV ${BUILD_ENVIRONMENT}
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV PYTHONDONTWRITEBYTECODE=1
ENV POETRY_VERSION=1.2.2
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_CACHE_DIR='/var/cache/pypoetry'
ENV POETRY_HOME='/usr/local'

WORKDIR ${APP_HOME}

RUN groupadd -g "${GID}" -r web \
  && useradd -d $APP_HOME -g web -l -r -u "${UID}" web \
  && chown web:web -R $APP_HOME \
  # Static files:
  && mkdir -p '/var/www/static' \
  && chown -R web:web '/var/www/static'


RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev \
  # Other tools \
  curl bash \
  gettext \
  wait-for-it \
  brotli

RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
  && apt-get install --no-install-recommends -y nodejs \
  && npm install -g npm@9.1.2 \
  && npm install -g yarn

# Cleaning cache:
RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

RUN pip install iredis

RUN curl -sSL 'https://install.python-poetry.org' | POETRY_HOME='/usr/local' python - \
  && poetry --version

COPY --chown=web:web ./poetry.lock ./pyproject.toml ${APP_HOME}/

RUN cd ${APP_HOME} && poetry config virtualenvs.create false \
  && poetry install --without local --no-interaction --no-ansi


COPY --chown=web:web ./yarn.lock ./package.json ${APP_HOME}/

RUN yarn install

COPY --chown=web:web . ${APP_HOME}/

RUN yarn run build && rm -rf node_modules

COPY --chown=web:web ./compose/production/app/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY --chown=web:web ./compose/production/app/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start


COPY --chown=web:web ./compose/production/app/celery/worker/start /start-celery-workers
RUN sed -i 's/\r$//g' /start-celery-workers
RUN chmod +x /start-celery-workers


COPY --chown=web:web ./compose/production/app/celery/beat/start /start-celery-beat
RUN sed -i 's/\r$//g' /start-celery-beat
RUN chmod +x /start-celery-beat


COPY --chown=web:web ./compose/production/app/celery/flower/start /start-celery-flower
RUN sed -i 's/\r$//g' /start-celery-flower
RUN chmod +x /start-celery-flower

RUN chown -R web:web ${APP_HOME}

RUN mkdir -p /var/log \
  && mkdir -p /var/log/django

RUN chown -R web:web /var/log

USER web


ENTRYPOINT ["/entrypoint"]
