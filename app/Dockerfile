FROM python:3.8.6

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
RUN chmod +x main.py

CMD ["python", "main.py"]