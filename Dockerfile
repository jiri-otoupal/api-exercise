FROM python:3.11-slim-buster
EXPOSE 8000

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt


CMD ["python3", "-m" , "uvicorn", "main:app", "--host=0.0.0.0","--port=8000"]