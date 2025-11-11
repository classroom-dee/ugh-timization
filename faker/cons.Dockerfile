FROM python:3.12-slim

COPY fake_consumer.py requirements.txt /

WORKDIR /

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "fake_consumer.py"]