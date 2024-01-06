dev:
    poetry run python manage.py runserver 0.0.0.0:8000

lint:
    poetry run pre-commit run --all-files

celery:
    poetry run watchmedo auto-restart  --directory=server --recursive --pattern '*.py' -- -- celery --app server worker -E -l INFO -Q celer

makemigrations:
    poetry run python manage.py makemigrations

migrate:
    poetry run python manage.py migrate

dbshell:
    poetry run python manage.py dbshell

notebook:
    DJANGO_ALLOW_ASYNC_UNSAFE=true poetry run python manage.py shell_plus --notebook --no-browser

shell:
    poetry run python manage.py shell_plus

up:
    docker-compose -f development.yml up -d

down:
    docker-compose -f development.yml down
