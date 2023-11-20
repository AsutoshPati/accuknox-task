# base image
FROM python:3.9

# setup environment variable
ENV DockerHOME=/home/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create work directory
# RUN #mkdir -p $DockerHOME

# Set the working directory to /app
WORKDIR $DockerHOME

# copy whole project to docker home directory.
COPY . $DockerHOME

# install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# expose the port where the Django app runs
EXPOSE 8000

# start server
CMD python manage.py runserver 0.0.0.0:8000
