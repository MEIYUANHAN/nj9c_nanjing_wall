web: gunicorn nanjing_wall_project.wsgi --bind 0.0.0.0:$PORT --config gunicorn.conf.py
release: python manage.py collectstatic --noinput && python manage.py migrate --noinput
