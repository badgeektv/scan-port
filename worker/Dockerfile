FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY ../backend/app ./app
CMD ["celery","-A","app.workers.tasks","worker","--loglevel=info"]
