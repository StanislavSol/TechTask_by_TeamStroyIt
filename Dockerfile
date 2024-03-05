FROM python:3.11-alpine

COPY ./requirements.txt .

RUN pip install -r ./requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--reload"]
