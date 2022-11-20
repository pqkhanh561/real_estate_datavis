from django.db import models


class Property(models.Model):
    num_bedroom = models.IntegerField()
    num_bathroom = models.IntegerField()
    area = models.DecimalField(max_digits=19, decimal_places=2)
    direction = models.TextField()
    status = models.TextField()
    license = models.TextField()
    width = models.DecimalField(max_digits=19, decimal_places=2)
    height = models.DecimalField(max_digits=19, decimal_places=2)
    road_width = models.DecimalField(max_digits=19, decimal_places=2)  # Do rong hem
    structure = models.TextField()
    year = models.IntegerField()
    front_width = models.DecimalField(max_digits=19, decimal_places=2)  # Do rong mat tien duong


class Utility(models.Model):
    near_market = models.BooleanField()
    near_school = models.BooleanField()
    near_center = models.BooleanField()
    good_design = models.BooleanField()
    security = models.BooleanField()
    near_front_road = models.BooleanField()
    near_hospital = models.BooleanField()
    near_park = models.BooleanField()
    parking = models.BooleanField()
    through_road = models.BooleanField()
    fast_trade = models.BooleanField()
    open_house = models.BooleanField()  # Nở hậu
    two_small_roads = models.BooleanField()
    two_roads = models.BooleanField()


class House(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.TextField()
    address = models.TextField()
    total_price = models.DecimalField(max_digits=19, decimal_places=2)
    unit_price = models.DecimalField(max_digits=19, decimal_places=2)
    property = models.ForeignKey('Property', on_delete=models.SET_NULL, null=True)
    utility = models.ForeignKey('Utility', on_delete=models.SET_NULL, null=True)
