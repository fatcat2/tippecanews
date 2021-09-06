# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.7

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . .

# Install production dependencies.
RUN pip install -r requirements.txt
RUN pip install gunicorn

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.

ENV PORT=PORT
ENV NEWS_API_KEY=KEY
ENV DAILY_ARTICLE_COUNT=1
ENV POSTGRES_USERNAME=USER
ENV POSTGRES_HOST=HOST
ENV POSTGRES_PASSWORD=POSTGRES_PASSWORD
ENV POSTGRES_DATABASE=POSTGRES_DATABASE
ENV POSTGRES_PORT=5432

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 main:tippecanews
