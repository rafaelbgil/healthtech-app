#imagem base
FROM alpine:3.18.4

#workdir
WORKDIR /app
COPY . /app
COPY docker-auxiliar-files/settings.py /app/healthtech/

RUN apk add --no-cache gcc python3 python3-dev linux-headers musl-dev pcre-dev py3-mysqlclient mariadb-dev py3-pip tzdata && pip3 install --no-cache-dir -r requirements.txt 
#RUN python manage.py collectstatic --noinput --no-post-process

EXPOSE 8000


CMD ["uwsgi", "--ini", "uwsgi.ini"]
