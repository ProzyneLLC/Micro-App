FROM python:3.6-buster

WORKDIR /Main

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "Main.py"]