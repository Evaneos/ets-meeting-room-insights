FROM python:3-alpine

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt

# Install python dependencies
RUN python -m pip install -r requirements.txt

COPY ./main.py ./.env /app/

CMD ["python", "main.py"]
