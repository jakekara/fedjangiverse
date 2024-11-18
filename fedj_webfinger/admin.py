from django.contrib import admin

from .models import LinkProperty, Subject, Alias, Link, Property, LinkTitle

class AliasInline(admin.TabularInline):
    model = Alias
    extra = 1

class PropertyInline(admin.TabularInline):
    model = Property
    extra = 1

class LinkTitleInline(admin.StackedInline):
    model = LinkTitle
    extra = 1

class LinkPropertyInline(admin.StackedInline):
    model = LinkProperty
    extra = 1

class LinkAdmin(admin.ModelAdmin):
    inlines = [LinkTitleInline, LinkPropertyInline]
    model = Link

class LinkInline(admin.StackedInline):
    model = Link
    show_change_link = True
    extra = 1

class SubjectAdmin(admin.ModelAdmin):
    inlines = [AliasInline, PropertyInline, LinkInline]

    pass

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Link, LinkAdmin)
