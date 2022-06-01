#!/bin/sh

if [ ! -f config/env/.env.local ]
then
  export $(cat config/env/.env.local | xargs)
fi

cd src/python/walterone

python manage.py flush --no-input
python manage.py migrate
python manage.py runserver
