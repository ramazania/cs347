# Alpine is a very small/lightweight Linux distribution
# We are starting from an alpine image with Python 3 installed
FROM python:3.7-alpine

# The WORKDIR command both creates a directory in the container 
# and sets that directory to be the current directory for all further commands
WORKDIR /code

# We set some Environment variables in the container which Flask uses
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# We install Flask and requests in the container using Pip
RUN pip install flask
RUN pip install requests

# We want port 5000 (the default Flask port) to be used outside the container
EXPOSE 5000

# We copy everything in the current directory on our machine 
# ... into the working directory in the container 
# (In particular, this includes app.py)
COPY . .

# When the container starts running,
#    This is the command that we want to be executed
#       flask run
CMD ["flask", "run"] 

# Note: The following also works ...
#   CMD ["python3", "app.py"]
 