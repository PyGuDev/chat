FROM python:3.8

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY .. ./

RUN pip install --no-cache-dir -r requirements.txt
RUN alembic upgrade head

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]
