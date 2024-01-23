FROM python:3.7-alpine

WORKDIR /usr/src/frontend

COPY . .

RUN pip install mysql-connector-python
RUN pip install Flask

EXPOSE 5500

CMD ["python3", "webapp.py"]