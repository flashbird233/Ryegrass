# Remove the records of ryegrass from the database
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ryegrass.settings')
django.setup()

from Breathe_Ease_Home.models import Ryegrass

Ryegrass.objects.all().delete()
