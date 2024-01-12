# start by pulling the python image
FROM python:3.11-alpine

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY dRail.py /app/app.py
COPY templates /app/templates

# configure the container to run in an executed manner
EXPOSE 5000
CMD [ "flask", "run", "--host=0.0.0.0" ]
