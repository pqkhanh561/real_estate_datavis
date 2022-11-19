from django.db import models


class Property(models.Model):
    num_bedroom = models.IntegerField()
    num_bathroom = models.IntegerField()
    area = models.DecimalField()
    direction = models.TextField()
    status = models.TextField()
    license = models.TextField()
    width = models.DecimalField()
    height = models.DecimalField()
    road_width = models.DecimalField()  # Do rong hem
    structure = models.TextField()
    year = models.IntegerField()
    front_width = models.DecimalField()  # Do rong mat tien duong


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
    total_price = models.DecimalField()
    unit_price = models.DecimalField()
    property = Property()
    utility = Utility()
