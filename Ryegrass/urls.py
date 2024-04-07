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
]
