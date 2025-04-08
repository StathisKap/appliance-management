web: gunicorn app_manager.wsgi --log-file -
release: python manage.py makemigrations && python manage.py migrate
