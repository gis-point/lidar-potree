#!/bin/bash
cd project

ApiDeploy()
{
    python manage.py migrate --noinput
    python manage.py initialize_buckets
    python manage.py loaddata */fixtures/*.json
    uwsgi --ini uwsgi.ini
}

Api()
{
    python manage.py makemigrations --noinput
    python manage.py migrate --noinput
    python manage.py collectstatic --noinput
    python manage.py loaddata */fixtures/*.json
    python manage.py initialize_buckets
    python manage.py runserver 0.0.0.0:8000 
}

Daphne()
{
    daphne config.asgi:application --port 10000 --bind 0.0.0.0 -v2
}

CeleryWorker()
{
    git clone https://github.com/potree/PotreeConverter.git /usr/src/potree_backend/project/PotreeConverter
    mkdir /usr/src/potree_backend/project/PotreeConverter/build 
    cd /usr/src/potree_backend/project/PotreeConverter/build 
    cmake .. 
    make 
    cd /usr/src/potree_backend/project
    celery -A config worker --loglevel=INFO --concurrency=8 -O fair -P prefork -n cel_app_worker
}

CeleryBeat()
{
    celery -A config beat -l info 
}


case $1
in
    api) Api ;;
    api-deploy) ApiDeploy;;
    celery-worker) CeleryWorker ;;
    celery-beat) CeleryBeat ;;
    daphne) Daphne;;
    *) exit 1 ;;
esac