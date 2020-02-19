FROM python:3.7-alpine3.10
ENV PYTHONUNBUFFERED=1 \
    FLASK_HOST="0.0.0.0" \
    FLASK_PORT=5000
EXPOSE ${FLASK_PORT}
WORKDIR /service
COPY requirements.txt /service/
RUN pip install -r /service/requirements.txt
COPY . /service/
ENTRYPOINT [ "python", "app.py" ]
