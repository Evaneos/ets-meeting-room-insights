FROM python:3-alpine

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt

RUN apk add --no-cache alpine-sdk

# Install python dependencies
RUN python -m pip install -r requirements.txt

COPY ./main.py ./.env /app/

CMD ["python", "main.py"]
