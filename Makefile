SETTINGS=page_exporter.settings.testing
BUILDDIR=~build
PYTHONPATH=${PWD}
BUILD_NUMBER=0
DBNAME=page_exporter
DBENGINE?=postgres

DJANGO_17?='django>=1.7,<1.8'
DJANGO_18?='django>=1.8,<1.9'
DJANGO_DEV=git+https://github.com/django/django.git


mkbuilddir:
	mkdir -p ${BUILDDIR}


help:
	@echo 'Makefile for spreader                                                  '
	@echo '                                                                       '
	@echo 'Usage:                                                                 '
	@echo '   make develop                     setup development environment      '
	@echo '   make install-deps                install requirements               '
	@echo '   make setup-git                   install git hooks                  '
	@echo '   make clean                       remove the generated files         '
	@echo '   make fullclean                   clean + remove .tox .cache         '
	@echo '   make locale                      django makemessages                '
	@echo '   make test                        run tests                          '
	@echo '   make flake8                      run flake8                         '
	@echo '   make pep8                        run pep8                           '
	@echo '   make coverage                    run coverage                       '
	@echo '   make init-db                     destroy/create database            '
	@echo '   make init-demo                   destroy/create demo environment    '
	@echo '   rtd                              trigger ReadTheDocs build          '
	@echo '   jenkins                          launch jenkins                     '
	@echo '                                                                       '
	@echo '   make serve                       run the full stack with circus     '
	@echo '   make start                       start the stack                    '
	@echo '   make stop                        sttop the stack                    '
	@echo '                                                                       '
	@echo '                                                                       '


develop:
	make install-deps

install-deps:
	pip install -qe .


locale:
	@cd page_exporter && django-admin.py makemessages -l en
	@cd page_exporter && PYTHONPATH=".." django-admin.py compilemessages --settings=${SETTINGS}


clean:
	# cleaning
	@rm -rf ${BUILDDIR} dist *.egg-info .coverage .pytest MEDIA_ROOT MANIFEST .cache *.egg build STATIC
	@find . -name __pycache__ -prune | xargs rm -rf
	@find . -name "*.py?" -o -name "*.orig" -o -name "*.min.min.js" -o -name "*.min.min.css" -prune | xargs rm -rf
	@rm -f coverage.xml flake.out pep8.out pytest.xml


build: locale

qa: coverage pep8 lint clonedigger

coverage: mkbuilddir
	py.test --cov-report=xml --junitxml=pytest.xml --cov-config=tests/.coveragerc --cov page_exporter

intersphinx:
	@sphinx-build -b html docs/ ${BUILDDIR}/docs/
	docs/intersphinx.py get ${BUILDDIR}/docs/objects.inv -p page_exporter -i docs/intersphinx.rst

docs: mkbuilddir intersphinx
	rm -fr docs/apidocs
	sphinx-apidoc page_exporter -H page_exporter -o docs/apidocs
	sphinx-build -n docs/ ${BUILDDIR}/docs/
ifdef BROWSE
	firefox ${BUILDDIR}/docs/index.html
endif


install-django:
	# installing Django==${DJANGO}
	@sh -c "if [ '${DJANGO}' = '1.7.x' ]; then pip install ${DJANGO_17}; fi"
	@sh -c "if [ '${DJANGO}' = '1.8.x' ]; then pip install ${DJANGO_18}; fi"
	@sh -c "if [ '${DJANGO}' = 'dev' ]; then pip install -q ${DJANGO_DEV}; fi"
	@echo "# installed  Django=="`django-admin.py --version`


init-db:
	# initializing '${DBENGINE}' database '${DBNAME}'

	@sh -c "if [ '${DBENGINE}' = 'postgres' ]; then psql -c 'DROP DATABASE IF EXISTS ${DBNAME};' -U postgres; fi"
	@sh -c "if [ '${DBENGINE}' = 'postgres' ]; then psql -c 'CREATE DATABASE ${DBNAME};' -U postgres; fi"
	@sh -c "if [ '${DBENGINE}' = 'postgres' ]; then pip install -q psycopg2; fi"


pep8: mkbuilddir
	pep8 page_exporter | tee ${BUILDDIR}/pep8.out


clonedigger: mkbuilddir
	clonedigger page_exporter -l python -o ${BUILDDIR}/clonedigger.html --ignore-dir=migrations,tests --fast


flake8: mkbuilddir
	flake8 --format pylint page_exporter | tee ${BUILDDIR}/flake.out


test:
	py.test -vvvvv


ci_test: clean mkbuilddir install-deps install-django init-db
	@$(MAKE) --no-print-directory coverage flake8 pep8 clonedigger


.PHONY: build docs
