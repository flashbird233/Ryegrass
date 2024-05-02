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
from django.urls import path

# from django.views import login
import Breathe_Ease_Home.views

urlpatterns = [
    path('', Breathe_Ease_Home.views.login_view, name='login'),
    path('home/', Breathe_Ease_Home.views.home, name='home'),
    path('map/', Breathe_Ease_Home.views.rye_map),
    path('cloth_view/', Breathe_Ease_Home.views.cloth_view, name='cloth_view'),
    path('base/', Breathe_Ease_Home.views.base),
    path('update_ryedb', Breathe_Ease_Home.views.update_ryegrass, name='update_ryegrass'),
    path('cloth_edu/', Breathe_Ease_Home.views.cloth_edu, name='cloth_edu'),
    path('Allergy_Hub/', Breathe_Ease_Home.views.allergy_hub, name='allergy_hub'),
    path('Allergy_Hub/symptom_relief_form', Breathe_Ease_Home.views.symptom_relief_form, name='symptom_relief_form'),
    path('Allergy_Hub/symptom_stats_form', Breathe_Ease_Home.views.symptom_stats_form, name='symptom_stats_form'),
    path('reminder_calendar/', Breathe_Ease_Home.views.generate_calendar_form, name='reminder_form'),
    path('map/api/locations', Breathe_Ease_Home.views.get_locations, name='get_locations'),
]
