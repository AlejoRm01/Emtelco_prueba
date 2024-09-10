FROM python:3.12-alpine

WORKDIR /app

COPY ./requirements.txt ./
COPY ./logs /logs 
RUN pip install -r requirements.txt

RUN pip install requests

COPY . .

EXPOSE 8000

RUN python manage.py migrate
RUN coverage run --source='.' manage.py test && coverage report && coverage html

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
