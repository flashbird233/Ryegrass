# Generated by Django 5.0.4 on 2024-04-14 23:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Breathe_Ease_Home', '0008_recommend_symptom_symptom_recommends_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Symptom_statistics',
            new_name='SymptomStatistics',
        ),
    ]