FROM python:3.12-alpine

WORKDIR /app

RUN pip install mysql-connector-python

RUN adduser -D appuser

COPY app.py .

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

CMD ["python3","app.py"]
