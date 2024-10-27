from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Resource(models.Model):

    uri = models.CharField(max_length=512, unique=True, null=False, blank=False)

    def __str__(self):
        return self.uri

class Alias(models.Model):

    class Meta:
        verbose_name_plural = "Aliases"

    account = models.ForeignKey(Resource, on_delete=models.CASCADE)

    value = models.CharField(max_length=512, unique=True, null=False, blank=False)


class Link(models.Model):

    account = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name="links")

    rel = models.CharField(max_length=512, null=False, blank=False)
    href = models.CharField(max_length=2048, null=False, blank=False)
    type = models.CharField(max_length=2048, null=True, blank=True)

class Property(models.Model):

    class Meta:
        verbose_name_plural = "Properties"

    parent = models.ForeignKey(Link, on_delete=models.CASCADE)
    key = models.CharField(max_length=512, unique=True, null=False, blank=False)
    value = models.CharField(max_length=512, unique=True, null=False, blank=False)
