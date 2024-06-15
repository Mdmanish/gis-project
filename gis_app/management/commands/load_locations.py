import csv
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from gis_app.models import Location

class Command(BaseCommand):
	help = 'Load locations from CSV file'

	def handle(self, *args, **kwargs):
		with open('locations CSV file.csv', 'r', encoding='utf-8-sig') as file:
			reader = csv.DictReader(file)
			sett = set()
			for row in reader:
				if not row['name'] or not row['latitude'] or not row['longitude']:
					self.stdout.write(self.style.WARNING(f'Skipping row with missing required data: {row}'))
					continue
				try:
					latitude = float(row['latitude'])
					longitude = float(row['longitude'])
				except ValueError:
					self.stdout.write(self.style.WARNING(f'Skipping row with invalid coordinates: {row}'))
					continue

				coordinates = (latitude, longitude)
				if coordinates in sett:
					continue
				sett.add(coordinates)
				name = row['name']
				description = row['description'] if row['description'] else 'No description available'
				point = Point(longitude, latitude)

				Location.objects.create(name=name, description=description, coordinates=point)

		self.stdout.write(self.style.SUCCESS('Successfully loaded locations data'))
