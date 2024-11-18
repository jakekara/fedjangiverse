# Fedjangiverse

> Fediverse social web stuff written in Django

# Demo site quick start

The `fedjangiverse_site` folder has a demo site that
uses all of the apps in developed in this repo. To run
the demo site, follow these steps:

Create a virtualenv, using whatever tool you like. I like
`pyenv`:

```shell
pyenv virtualenv 3.12 fedjangiverse
```

Install requirements:

```shell
pip install -r requirements.txt
```

This will install Django and all of the apps from
this repo in editable mode, so changes will be reflected
right away.

Run migrations

```shell
python manage.py migrate
```

Add a super user so you can get into the admin panel:

```shell
python manage.py createsuperuser
```

Follow the prompts, then start the django server:

```shell
python manage.py runserver
```

Browse to the admin page (http://127.0.0.1:8000/admin/).

# Apps

This repo contains/will contain Django apps for different
Fediverse/Social Web implementations in Django.

As much as possible, I will break features into separate
apps to the extent that they're useful in isolation. 

## fedj_webfinger

The only app for now is `fedj_webfinger`, which implements
a webfinger service. This can be used without any other
Social Web features.

When you follow the quickstart guide above, you can
add subjects in the Django admin (http://127.0.0.1:8000/admin/),
and then query them according to the [Webfinger RFC](https://datatracker.ietf.org/doc/html/rfc7033).

For example, if you add a Subject `acct:you@example.domain`
via the admin panel, and browse to 
`http://127.0.0.1:8000/webfinger?resource=acct:you@example.domain`, you will get a response listing the Subject, along
with any Aliases, Properties and Links. These terms are all
used consistently with the [Webfinger RFC](https://datatracker.ietf.org/doc/html/rfc7033).
