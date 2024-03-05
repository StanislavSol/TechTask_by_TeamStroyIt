build:
	./build.sh

dev:
	poetry run uvicorn app.main:app --reload

lint:
	poetry run flake8

start:
	poetry run uvicorn app.main:app --host 0.0.0.0 --port 10000
