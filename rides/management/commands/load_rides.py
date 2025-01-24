import csv
from django.core.management.base import BaseCommand
from rides.models import User, Ride

class Command(BaseCommand):
    help = 'Load rides from a CSV file'

    def handle(self, *args, **kwargs):
        with open('rides.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                rider = User.objects.get(id_user=row['id_rider'])
                driver = User.objects.get(id_user=row['id_driver'])
                Ride.objects.create(
                    status=row['status'],
                    id_rider=rider,
                    id_driver=driver,
                    pickup_latitude=row['pickup_latitude'],
                    pickup_longitude=row['pickup_longitude'],
                    dropoff_latitude=row['dropoff_latitude'],
                    dropoff_longitude=row['dropoff_longitude'],
                    pickup_time=row['pickup_time']
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded rides'))