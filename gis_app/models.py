from django.contrib.gis.db import models


class Location(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField()
	coordinates = models.PointField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name


class Boundary(models.Model):
	name = models.CharField(max_length=255)
	area = models.PolygonField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name
