# Python FastAPI for Serving Parcel Data
FROM python:3.8-slim-buster

LABEL maintainer='Branson Fox <bransonfox@umsl.edu>'

# Environmental Variables

## For Connecting to DB
ENV DB_HOST='localhost'
ENV DB_PORT=5432
ENV DB_USER='postgres'
ENV DB_PASS='postgres'
ENV DB_NAME='redb'

# Install Python Dependencies
RUN mkdir -p /redb/api
WORKDIR /redb/api
COPY requirements.txt /redb/api/requirements.txt

RUN pip install -r /redb/api/requirements.txt

# Copy API Files
COPY main.py /redb/api/main.py
COPY models/models.py /redb/api/models/models.py
COPY config.py /redb/api/config.py

EXPOSE 3001

# Start Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3001"]
