FROM python:3.9

WORKDIR /app

COPY requirements/* requirements/
RUN pip3 install -r requirements/development.txt

COPY . .

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
