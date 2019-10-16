FROM python:3.7-alpine
WORKDIR /code

RUN apk update && apk add --no-cache postgresql-dev gcc python3-dev musl-dev make linux-headers

ENV PYTHONPATH "${PYTHONPATH}:/code"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["make", "run"]