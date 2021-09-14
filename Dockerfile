FROM python:3.7.1

LABEL Author="Abel Orihuela"
LABEL E-mail="abelorihuelamendoza@hotmail.com"
LABEL version="0.0.1"

ENV FLASK_APP "app.py"
ENV FLASK_ENV "production"
ENV FLASK_DEBUG False

RUN mkdir /app-flask
WORKDIR /app-flask

COPY Pip* /app-flask/

RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --dev --system --deploy --ignore-pipfile

ADD . /app-flask

# EXPOSE 5000

# CMD flask run --host=0.0.0.0

ENTRYPOINT gunicorn --access-logfile - --limit-request-field_size 0 --timeout=900 --workers=4 app:app --bind :5000