FROM python:3.7-slim

WORKDIR /APP

# Install libraries
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# Copy app
COPY ./ ./

ENTRYPOINT [ "python", "./main.py" ]
