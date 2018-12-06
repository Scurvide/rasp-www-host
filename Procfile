release: python RaspWWW/manage.py migrate
web: gunicorn RaspWWW.RaspWWW.wsgi.application --log-file -
