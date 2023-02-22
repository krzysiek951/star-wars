#!/usr/bin/make -f

migrate:
	docker-compose run --rm src sh -c "python manage.py migrate"

migrations:
	docker-compose run --rm src sh -c "python manage.py makemigrations"

start:
	docker-compose up

stop:
	docker-compose stop

down:
	docker-compose down -v

reset-db:
	docker-compose run --rm src sh -c "python manage.py flush --no-input"

test:
	docker-compose run --rm src sh -c "coverage run -m pytest"

test-report:
	docker-compose run --rm src sh -c "coverage report -m"
