from django.contrib import admin

from dsl.models import DslRequest


class DslRequestAdmin(admin.ModelAdmin):
    list_display = ('postcode', 'housenumber', 'housenumber_add', 'created')
    readonly_fields = ('created',)


admin.site.register(DslRequest, DslRequestAdmin)
