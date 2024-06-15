from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Location, Boundary
from django.contrib.gis.geos import Point, Polygon

class RegisterUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('username', 'email', 'password')
		extra_kwargs = {'password': {'write_only': True}}

class LoginUserSerializer(serializers.Serializer):
	username = serializers.CharField()
	password = serializers.CharField()

class LocationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Location
		fields = '__all__'

	def create(self, validated_data):
		coordinates_data = validated_data.pop('coordinates')
		coordinates = Point(coordinates_data['coordinates'][0], coordinates_data['coordinates'][1])
		location = Location.objects.create(coordinates=coordinates, **validated_data)
		return location

	def update(self, instance, validated_data):
		coordinates_data = validated_data.get('coordinates')
		if coordinates_data:
			instance.coordinates = Point(coordinates_data['coordinates'][0], coordinates_data['coordinates'][1])
		instance.name = validated_data.get('name', instance.name)
		instance.description = validated_data.get('description', instance.description)
		instance.save()
		return instance

class BoundarySerializer(serializers.ModelSerializer):
	class Meta:
		model = Boundary
		fields = '__all__'

	def create(self, validated_data):
		area_data = validated_data.pop('area')
		area = Polygon(area_data['coordinates'][0])
		boundary = Boundary.objects.create(area=area, **validated_data)
		return boundary

	def update(self, instance, validated_data):
		area_data = validated_data.get('area')
		if area_data:
			instance.area = Polygon(area_data['coordinates'][0])
		instance.name = validated_data.get('name', instance.name)
		instance.save()
		return instance
