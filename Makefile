server:
	python3 manage.py runserver
migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate
superuser:
	python3 manage.py createsuperuser
