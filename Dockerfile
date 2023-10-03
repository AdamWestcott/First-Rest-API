FROM python:3.11
EXPOSE 5000
WORKDIR /app
#Copys Requirements.txt into current folder
COPY  requirements.txt .
#installs all libaries in requirements.txt
RUN pip install -r requirements.txt
COPY . .
#Runs the flask app, host 0.0.0.0 allows external connections to the docker
CMD ["flask", "run","--host","0.0.0.0"] 