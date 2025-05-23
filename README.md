# Django with Postgres & Redis on Codespaces

This is a template repository for Django with PostgreSQL & Redis with a sample ___ project to get started. It is set up to be deployed on render.com

Create a new repository based on this template to start a new project.

## installing dependancies

```python
pip install -r requirements.txt
```

## To collect static files:

```python
python manage.py collectstatic
```

## To run this application:

```python
python manage.py runserver
```

## To set up admin access
```python
python manage.py createsuperuser
```

## To deploy on Render.com

REDIS is disabled initially. Uncomment relevant sections to use.

Create the following environment variabels in Render Dashboard. They will need to be set based on the .onrender.com domain

    - ALLOWED_HOSTS
    - CSRF_TRUSTED_ORIGINS 

If using django admin AND free Render plan, create the following environment variables in Render Dashboard

    - DJANGO_SUPERUSER_USERNAME
    - DJANGO_SUPERUSER_PASSWORD
    - DJANGO_SUPERUSER_EMAIL
    
Then uncomment createsuperuser command in build.sh for ONE DEPLOY ONLY (this is only necessary on free render accoutns without shell access)

## Credits

Template and project structure taken/modified from [Lithium](https://github.com/wsvincent/lithium)