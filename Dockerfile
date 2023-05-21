FROM python:3.9

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

WORKDIR /app/bad

RUN ./db_init.py
ENV FLASK_APP=vulpy.py
ENTRYPOINT ["python", "vulpy.py", "--host=0.0.0.0:5000"]
