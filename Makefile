.PHONY: setup run test build stop

setup:
	python3 -m venv .venv
	./.venv/bin/pip install -r requirements.txt
	cp .env.example .env

run:
	docker-compose up --build

stop:
	docker-compose down

test:
	docker-compose run api pytest tests/
