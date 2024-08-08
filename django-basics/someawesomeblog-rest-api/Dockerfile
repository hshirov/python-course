FROM python:3.12
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt --no-cache-dir
EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
