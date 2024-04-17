"""
URL configuration for Ryegrass project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve

import Breathe_Ease_Home.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Breathe_Ease_Home.views.home),  # Default path
    path('home/', Breathe_Ease_Home.views.home),
    path('map/', Breathe_Ease_Home.views.rye_map),
    re_path(r'static/(?P<path>.*)', serve, {"document_root": settings.STATIC_ROOT}, name="static"),
    path('cloth_edu/', Breathe_Ease_Home.views.cloth_edu),
    path('base/', Breathe_Ease_Home.views.base),
    path('update_ryedb', Breathe_Ease_Home.views.update_ryegrass, name='update_ryegrass'),
    path('chat/', Breathe_Ease_Home.views.customer_support_chat, name='customer_support_chat'),
    path('cloth_sug', Breathe_Ease_Home.views.suggest_clothing, name='suggest_clothing'),
    path('Allergy_Hub/', Breathe_Ease_Home.views.allergy_hub, name='allergy_hub'),
    path('Allergy_Hub/symptom_relief_form', Breathe_Ease_Home.views.symptom_relief_form, name='symptom_relief_form'),
    path('Allergy_Hub/symptom_stats_form', Breathe_Ease_Home.views.symptom_stats_form, name='symptom_stats_form'),
    path('reminder_calendar/', Breathe_Ease_Home.views.generate_calendar_form, name='reminder_form'),
]
