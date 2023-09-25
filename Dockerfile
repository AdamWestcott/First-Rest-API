FROM python:3.11
EXPOSE 5000
WORKDIR /app
#installs flask
RUN pip install flask
COPY . .
#Runs the flask app, host 0.0.0.0 allows external connections to the docker
CMD ["flask", "run","--host","0.0.0.0"] 