from django.db import models


# Create your models here.

# postcode model
class Location(models.Model):
    # id
    loc_id = models.IntegerField(primary_key=True, auto_created=True, null=False)
    # postcode
    loc_postcode = models.CharField(max_length=5, default=None)
    # suburb
    loc_suburb = models.CharField(max_length=100, default=None)
    # state
    loc_state = models.CharField(max_length=4, default=None)
    # latitude
    loc_lat = models.FloatField(max_length=9, default=None)
    # longitude
    loc_long = models.FloatField(max_length=9, default=None)

    # return postcode
    def __str__(self):
        return self.loc_postcode, ": ", self.loc_suburb, ", ", self.loc_state


# pyegrass record model
class Ryegrass(models.Model):
    # id
    rye_id = models.IntegerField(primary_key=True, auto_created=True, null=False)
    # latitude
    rye_lat = models.FloatField(max_length=10, default=0, null=False)
    # longitude
    rye_lon = models.FloatField(max_length=10, default=0, null=False)
    # rye_record_by
    rye_record_by = models.CharField(max_length=200, default=None, null=True)
    # datetime
    rye_date = models.DateTimeField(default=None, null=True)
    # rye_scientific_name
    rye_scientific_name = models.CharField(max_length=100, default=None, null=True)
    # rye_vernacular_name
    rye_vernacular_name = models.CharField(max_length=100, default=None, null=True)
    # rye_taxon_concept_id
    rye_taxon_concept_id = models.URLField(max_length=200, default=None, null=True)

    # return pyegrass record
    def __str__(self):
        return "{}, {}, {}".format(self.rye_lat, self.rye_lon, self.rye_date)


# symptom record model
class Symptom(models.Model):
    # id
    symptom_id = models.IntegerField(primary_key=True, auto_created=True, null=False)
    # title
    symptom_title = models.CharField(max_length=100, default=None, null=True)

    # return symptom record
    def __str__(self):
        return self.symptom_title


class Recommend(models.Model):
    recommend_id = models.IntegerField(primary_key=True, auto_created=True, null=False)
    recommend_title = models.CharField(max_length=100, default=None, null=True)

    def __str__(self):
        return self.recommend_title


class SymptomRecommends(models.Model):
    symp_rec_id = models.IntegerField(primary_key=True, auto_created=False, null=False)
    symptom_id = models.IntegerField(null=False)
    recommend_id = models.IntegerField(null=False)

    def __str__(self):
        return "{}, {}".format(self.symptom_id, self.recommend_id)


class SymptomStatistics(models.Model):
    symptom_id = models.IntegerField(primary_key=True, auto_created=False, null=False)
    symptom_count = models.IntegerField(null=False, default=0)

    def __str__(self):
        return "{}, {}".format(self.symptom_id, self.symptom_count)

class User(models.Model):
    password = models.CharField(max_length=128)