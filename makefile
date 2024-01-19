run:
	cd compbatya && python3 manage.py runserver
createmigr:
	cd compbatya && python3 manage.py makemigrations
migrate:
	cd compbatya && python3 manage.py migrate
admin:
	cd compbatya && python3 manage.py createsuperuser
all-tests:
	cd compbatya && python3 manage.py test .