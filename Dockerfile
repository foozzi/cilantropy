FROM python:3.7.8-stretch

ADD requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# adding application files
ADD . /webapp

# configure path /webapp to HOME-dir
ENV HOME /webapp
WORKDIR /webapp

ENTRYPOINT ["uwsgi"]
CMD ["--http", "0.0.0.0:8080", "--wsgi-file", "wsgi.py", "--callable", "app", "--processes", "1", "--threads", "8"]