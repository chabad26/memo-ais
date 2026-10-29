FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY lab ./lab
COPY tests ./tests
USER 10001:10001
CMD ["python", "-m", "lab.server", "--host", "0.0.0.0"]
