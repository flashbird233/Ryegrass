from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Location, Ryegrass


class RyegrassAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'update_button')

    def update_button(self, obj):
        return format_html('<button type="button" onclick="location.href=\'{}\'">Update</button>',
                           reverse('update_ryegrass', args=[obj.pk]))

    update_button.short_description = 'Update Button'
    update_button.allow_tags = True


admin.site.register(Location)
admin.site.register(Ryegrass, RyegrassAdmin)
