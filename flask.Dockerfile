FROM     python:3.8.0-buster 
ADD      ./ ./tmp
WORKDIR  /tmp/
RUN      pip install --upgrade pip
RUN      pip install -r back/requirements.txt
CMD      ["python", "back/manage.py db migrate"]
CMD      ["python", "back/manage.py db upgrade"]
CMD      ["python", "back/app.py"]