from django.db import models

# Create your models here.
class Map(models.Model):
	longitude = models.DecimalField(max_digits=35, decimal_places=28)
	latitude = models.DecimalField(max_digits=35, decimal_places=28)
	bound_up_right = models.DecimalField(max_digits=35, decimal_places=28)
	bound_up_left = models.DecimalField(max_digits=35, decimal_places=28)
	bound_down_right = models.DecimalField(max_digits=35, decimal_places=28)
	bound_down_left = models.DecimalField(max_digits=35, decimal_places=28)
	radius = models.FloatField()
	query_times = models.IntegerField()


class Place(models.Model):
	map_id = models.ForeignKey(Map)
	longitude = models.DecimalField(max_digits=35, decimal_places=28)
	latitude = models.DecimalField(max_digits=35, decimal_places=28)
	radius = models.FloatField()
	query_times = models.IntegerField()