import csv
from django.core.management.base import BaseCommand
from rides.models import User

class Command(BaseCommand):
    help = 'Load users from a CSV file'

    def handle(self, *args, **kwargs):
        with open('users.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                User.objects.create(
                    role=row['role'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    username=row[f'email'],
                    email=row['email'],
                    phone_number=row['phone_number']
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded users'))
