DJANGO_KEY ?= xxxdsadsadasxx
RABBIT_SERVER ?= 192.168.0.110

export DJANGO_KEY RABBIT_SERVER
test:
	coverage run --source=./  ./manage.py test 
	coverage html
test-xml:
	coverage run --source=./  ./manage.py test
	coverage xml
run:
	python manage.py runserver 0.0.0.0:8000

run-prod:
	uwsgi --ini uwsgi.ini

update-db:
	python manage.py makemigrations
	python manage.py migrate
	python manage.py makemigrations agenda
	python manage.py makemigrations paciente
	python manage.py makemigrations medico
	python manage.py migrate

