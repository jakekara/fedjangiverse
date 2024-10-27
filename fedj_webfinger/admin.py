from django.contrib import admin

from .models import Resource, Alias, Link, Property


class AliasInline(admin.TabularInline):
    model = Alias


class PropertyInline(admin.TabularInline):
    model = Property


class LinkInline(admin.StackedInline):
    model = Link
    inlines = [PropertyInline]
    show_change_link = True


class LinkAdmin(admin.ModelAdmin):
    pass


class ResourceAdmin(admin.ModelAdmin):
    inlines = [AliasInline, LinkInline]


admin.site.register(Resource, ResourceAdmin)
admin.site.register(Link)
# admin.site.register(Link, LinkAdmin)
