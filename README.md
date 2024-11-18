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

# Apps

This repo contains/will contain Django apps for different
Fediverse/Social Web implementations in Django.

As much as possible, I will break features into separate
apps to the extent that they're useful in isolation. 

## fedj_webfinger

The only app for now is `fedj_webfinger`, which implements
a webfinger service. This can be used without any other
Social Web features.
