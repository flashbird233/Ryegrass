# Generated by Django 5.0.3 on 2024-05-01 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Breathe_Ease_Home', '0009_rename_symptom_statistics_symptomstatistics'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
            ],
        ),
    ]