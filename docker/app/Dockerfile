
from python:3.6

RUN mkdir app

COPY .app/ app/

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt  

RUN pip install gunicorn

CMD [ "gunicorn", "-w 4", "app:app" ]