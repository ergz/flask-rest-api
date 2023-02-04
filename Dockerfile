FROM python:3.11
EXPOSE 5000
WORKDIR /app

# currently in /app
COPY . . 

RUN pip install -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0"]

