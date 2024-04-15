# Generated by Django 5.0.4 on 2024-04-14 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Breathe_Ease_Home', '0007_alter_ryegrass_rye_lat_alter_ryegrass_rye_lon'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recommend',
            fields=[
                ('recommend_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('recommend_title', models.CharField(default=None, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Symptom',
            fields=[
                ('symptom_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('symptom_title', models.CharField(default=None, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SymptomRecommends',
            fields=[
                ('symp_rec_id', models.IntegerField(primary_key=True, serialize=False)),
                ('symptom_id', models.IntegerField()),
                ('recommend_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Symptom_statistics',
            fields=[
                ('symptom_id', models.IntegerField(primary_key=True, serialize=False)),
                ('symptom_count', models.IntegerField(default=0)),
            ],
        ),
    ]
