FROM python:3
COPY ./src ./server
RUN pip install -r ./server/requirements.txt
CMD ["python3", "./server/server.py"]
