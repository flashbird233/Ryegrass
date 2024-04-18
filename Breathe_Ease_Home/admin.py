from django.contrib import admin

from .models import Location, Ryegrass, Symptom, Recommend, SymptomRecommends, SymptomStatistics

admin.site.register(Location)
admin.site.register(Ryegrass)
admin.site.register(Symptom)
admin.site.register(Recommend)
admin.site.register(SymptomRecommends)
admin.site.register(SymptomStatistics)
