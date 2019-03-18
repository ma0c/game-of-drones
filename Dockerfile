FROM python:3.7-alpine

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt

ADD . /code/
RUN python manage.py migrate
RUN python manage.py configure_game rock_paper_scissors.json
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
