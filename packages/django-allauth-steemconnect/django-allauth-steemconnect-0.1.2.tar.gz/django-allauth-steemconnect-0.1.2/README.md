# django-allauth-steemconnect

Steemconnect provider for django-allauth.

## Installation

```shell
pip install django-allauth-steemconnect
```

## Quick start

1. Add "django_allauth_steemconnect" to your INSTALLED_APPS setting like this::

```python
    INSTALLED_APPS = [
        ...
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'django_allauth_steemconnect.providers.steemconnect',
    ]
```

2. Include the polls URLconf in your project urls.py like this::

```python
    path('accounts/', include('allauth.urls')),
```

3. Run `python manage.py migrate` to create the allauth models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a social app (you'll need the Admin app enabled).
