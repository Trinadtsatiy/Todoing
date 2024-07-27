FROM python:3.12

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . .

RUN chmod 755 app/scripts/start.sh

CMD ["sh", "start.sh"]