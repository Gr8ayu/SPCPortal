# Use the official Python image from the Docker Hub
FROM python:3.8.2

# These two environment variables prevent __pycache__/ files.
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Make a new directory to put our code in.
RUN mkdir /code

# Change the working directory. 
# Every command after this will be run from the /code directory.
WORKDIR /code

# Copy the requirements.txt file.
COPY ./requirements.txt /code/

# Upgrade pip
RUN pip install --upgrade pip

# Install the requirements.
RUN pip install -r requirements.txt


# Copy the rest of the code. 
COPY . /code/

# expose the port 8000
EXPOSE 8000


# define the default command to run when starting the container
CMD ["gunicorn",  "--bind", ":8000", "spcportal.wsgi:application"]
#CMD ["pytest"]
# CMD [ "./manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["bash", "./run.sh"]
