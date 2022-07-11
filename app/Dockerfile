FROM python:3.8.10-alpine

RUN pip3 install --upgrade pip

# copy src to container
WORKDIR /usr/app
COPY . .


# Download flask and pymongo
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install "pymongo[srv]"

# export port 5000 to app's API.
EXPOSE 5000
EXPOSE 27017

# Run the application.
CMD ["python3", "src/app.py"]