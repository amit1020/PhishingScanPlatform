FROM python:latest

WORKDIR /app

COPY app_data/requirements2.txt .

RUN pip install --no-cache-dir -r requirements2.txt

COPY app_data/ .

CMD [ "python", "app.py" ]