from django.db import models


class Property(models.Model):
    num_bedroom = models.IntegerField(null=True)
    num_bathroom = models.IntegerField(null=True)
    area = models.DecimalField(max_digits=19, decimal_places=2, null=True)
    direction = models.TextField(null=True)
    status = models.TextField(null=True)
    license = models.TextField(null=True)
    width = models.DecimalField(max_digits=19, decimal_places=2, null=True)
    height = models.DecimalField(max_digits=19, decimal_places=2, null=True)
    road_width = models.DecimalField(max_digits=19, decimal_places=2, null=True)  # Do rong hem
    structure = models.TextField(null=True)
    year = models.IntegerField(null=True)
    front_width = models.DecimalField(max_digits=19, decimal_places=2, null=True)  # Do rong mat tien duong


class Utility(models.Model):
    near_market = models.BooleanField(null=True)
    near_school = models.BooleanField(null=True)
    near_center = models.BooleanField(null=True)
    good_design = models.BooleanField(null=True)
    security = models.BooleanField(null=True)
    near_front_road = models.BooleanField(null=True)
    near_hospital = models.BooleanField(null=True)
    near_park = models.BooleanField(null=True)
    parking = models.BooleanField(null=True)
    through_road = models.BooleanField(null=True)
    fast_trade = models.BooleanField(null=True)
    open_house = models.BooleanField(null=True)  # Nở hậu
    two_small_roads = models.BooleanField(null=True)
    two_roads = models.BooleanField(null=True)


class House(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.TextField()
    address = models.TextField()
    total_price = models.TextField()
    unit_price = models.TextField(null=True)
    property = models.ForeignKey('Property', on_delete=models.SET_NULL, null=True)
    utility = models.ForeignKey('Utility', on_delete=models.SET_NULL, null=True)

