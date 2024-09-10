FROM python:3.12-alpine

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install requests

COPY . .

EXPOSE 8000

RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
