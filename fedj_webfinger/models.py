"""
Data model for Webfinger

For more details see
https://www.rfc-editor.org/rfc/rfc7033#section-4.4
"""

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Subject(models.Model):

    """https://www.rfc-editor.org/rfc/rfc7033#section-4.4.1
    
   From RFC: The value of the "subject" member is a URI that identifies the entity
   that the JRD describes."""

    value = models.CharField(max_length=512, unique=True, null=False, blank=False, verbose_name="URI")

    def __str__(self):
        return self.value

class Alias(models.Model):
    """https://www.rfc-editor.org/rfc/rfc7033#section-4.4.2
    
    From RFC:  The "aliases" array is an array of zero or more URI strings that
   identify the same entity as the "subject" URI.
    """

    class Meta:
        verbose_name_plural = "Aliases"

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    value = models.CharField(max_length=512, unique=False, null=False, blank=False)


class Property(models.Model):

    """https://www.rfc-editor.org/rfc/rfc7033#section-4.4.3
    
    From RFC: The "properties" object comprises zero or more name/value pairs whose
    names are URIs (referred to as "property identifiers") and whose
    values are strings or null.  Properties are used to convey additional
    information about the subject of the JRD.  As an example, consider
    this use of "properties":

     "properties" : { "http://webfinger.example/ns/name" : "Bob Smith" }
     """

    class Meta:
        verbose_name_plural = "Properties"

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=512, unique=True, null=False, blank=False)
    value = models.CharField(max_length=512, unique=True, null=False, blank=False)

    def save(self, *args, **kwargs):
        """Prevent saving if there's already a LinkTitle
        with this name attached to the link"""
        if Property.objects.filter(subject=self.subject, name=self.name).exists():
            raise ValueError(f"Subject cannot have two Properties with the same name: '{self.name}'")

        super().save(*args, **kwargs)

class Link(models.Model):

    """
    https://www.rfc-editor.org/rfc/rfc7033#section-4.4.4

       The "links" array has any number of member objects, each of which
   represents a link [4].  Each of these link objects can have the
   following members:
    - rel
    - type
    - href
    - titles
    - properties
    """

    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="links"
    )
    rel = models.CharField(max_length=512, null=False, blank=False, help_text="relationship of link to subject")
    href = models.CharField(max_length=512, null=False, blank=False, help_text="uri of link")

    
    type = models.CharField(max_length=512, 
        null=True,
        blank=True,
        help_text="The media type of the dereferenced link. http://www.iana.org/assignments/media-types/media-types.xhtml"
    )

class LinkTitle(models.Model):
    """https://www.rfc-editor.org/rfc/rfc7033#section-4.4.4.4
    
    Internationalized name, value pair, where name is the language
    tag or 'und' and value is a human-readable string that describes the resource
    
    Example from RFC:
    {"en-us" : "The Magical World of Steve"}

    would have name "en-us" and value "The Magical World of Steve"
    """

    link = models.ForeignKey(Link, on_delete=models.CASCADE, related_name="titles")
    name = models.CharField(max_length=32, blank=False, null=False, default="und", help_text="must be a language code")
    value = models.CharField(max_length=512, blank=False, null=False)

    def save(self, *args, **kwargs):
        """Prevent saving if there's already a LinkTitle
        with this name attached to the link"""
        if LinkTitle.objects.filter(link=self.link, name=self.name).exists():
            raise ValueError(f"Link cannot have two LinkTitles with the same name: '{self.name}'")
        
        super().save(*args, **kwargs)


class LinkProperty(models.Model):
    """https://www.rfc-editor.org/rfc/rfc7033#section-4.4.4.5
    """

    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    name = models.CharField(max_length=32, blank=False, null=False)
    value = models.CharField(max_length=512, blank=False, null=False)

    def save(self, *args, **kwargs):
        """Prevent saving if there's already a LinkProperty
        with this name attached to the link"""
        if LinkProperty.objects.filter(link=self.link, name=self.name).exists():
            raise ValueError(f"Link cannot have two LinkProperties with the same name: '{self.name}'")
        
        super().save(*args, **kwargs)
