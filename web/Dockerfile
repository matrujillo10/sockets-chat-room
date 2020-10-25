FROM python:3.7-slim

RUN apt-get update && apt-get install curl -y

ARG APP_PATH=/var/www
RUN mkdir -p $APP_PATH
WORKDIR $APP_PATH

# Set env variables
ENV FLASK_ENV="production"

# Install libraries
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# Copy app
COPY ./ ./

RUN chmod +x ./entry_point.sh
ENTRYPOINT [ "./entry_point.sh" ]
