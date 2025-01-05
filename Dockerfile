FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src .

EXPOSE 8000
CMD [ "python3", "mysite/manage.py", "runserver", "0.0.0.0:8000" ]
