# pull official base image
FROM python:3.11.6

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_HOME /app

# set work directory
WORKDIR $APP_HOME

# install requirements
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy all files to work directory
COPY . .

# collect static files (Django REST Framework API)
RUN python manage.py collectstatic --noinput

# create django migrations
RUN python manage.py makemigrations

# expose port 8000
EXPOSE $PORT

# run project with gunicorn
CMD ["gunicorn", "modularAPI.wsgi"]
