from django.core.validators import MinValueValidator, MaxValueValidator
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
class Pyegrass(models.Model):
    # id
    pye_id = models.IntegerField(primary_key=True, auto_created=True, null=False)
    # latitude
    pye_lat = models.FloatField(max_length=10, default=None)
    # longitude
    pye_lon = models.FloatField(max_length=10, default=None)
    # datetime
    pye_datetime = models.DateTimeField(max_length=50, default=None, null=True)
    # year
    pye_year = models.IntegerField(default=None, null=True,
                                   validators=[MinValueValidator(1000), MaxValueValidator(2021)])
    # month
    pye_month = models.IntegerField(default=None, null=True,
                                    validators=[MinValueValidator(1), MaxValueValidator(12)])
    # day
    pye_day = models.IntegerField(default=None, null=True,
                                  validators=[MinValueValidator(1), MaxValueValidator(31)])
    # rye_record_by
    pye_record_by = models.CharField(max_length=200, default=None, null=True)
    # rye_country
    pye_country = models.CharField(max_length=50, default=None, null=True)
    # rye_country_code
    pye_country_code = models.CharField(max_length=10, default=None, null=True)
    # rye_scientific_name
    pye_scientific_name = models.CharField(max_length=100, default=None, null=True)
    # rye_vernacular_name
    pye_vernacular_name = models.CharField(max_length=100, default=None, null=True)

    # return pyegrass record
    def __str__(self):
        return self.pye_lat, ", ", self.pye_lon, ", ", self.pye_datetime
