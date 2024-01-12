run:
	cd compbatya && python3 manage.py runserver
createmigr:
	cd compbatya && python3 manage.py makemigrations
migrate:
	cd compbatya && python3 manage.py migrate
admin:
	cd compbatya && python3 manage.py createsuperuser
app:
	cd compbatya && python3 manage.py startapp