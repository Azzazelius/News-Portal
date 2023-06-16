FROM python:3.8
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]