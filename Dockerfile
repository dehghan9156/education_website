FROM python:3.10
ENV PYTHONUNBUFFERED=1
WORKDIR /web 
COPY requirements.txt .

RUN pip install -U pip
RUN pip install -r requirements.txt 

COPY . /web/

EXPOSE 8000
CMD [ "gunicorn","education_website.wsgi",":8000" ]