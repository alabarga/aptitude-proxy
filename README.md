# aptitude-django

## Getting started

- `git clone git@gitlab-internal.bsc.es:health-data/aptitude-proxy.git`
- `cd aptitude-proxy/`
- `python -m venv .venv`
- `source .venv/bin/activate`
- `cp aptitude/settings/local_template.py aptitude/settings/local.py`
- Edit `aptitude/settings/local.py`
- `python -m pip install -r requirements.txt`
- `python manage.py check`
- `python manage.py runserver`
- Go to http://localhost:8000/admin/
- Login as jmartin3/datos_cat


