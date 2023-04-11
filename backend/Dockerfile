FROM python:3.9.1
ADD . /app
WORKDIR /app
RUN pip install -r backend_logic/requirements.txt
CMD ["python3", "-m", "backend_logic.api"]