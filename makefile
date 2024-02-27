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
dump-db:
	cd compbatya && python3 manage.py dumpdata --indent=2 --exclude contenttypes -o db.json
load-db:
	cd compbatya && python3 manage.py loaddata db.json
celery:
	cd compbatya && celery -A compbatya worker -l INFO