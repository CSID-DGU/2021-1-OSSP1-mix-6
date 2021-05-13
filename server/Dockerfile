FROM python:3.6

# set a directory for the app
WORKDIR /app

# copy all the files to the container
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update
RUN apt-get install -y clang

# tell the port number the container should expose
EXPOSE 5000

# run the command
CMD ["python3", "./web.py"]
