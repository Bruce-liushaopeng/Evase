FROM python:3.9

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/
WORKDIR /app/

EXPOSE 5000

CMD ["python3", "-m", "flask", "run"]