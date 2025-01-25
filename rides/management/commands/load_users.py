import csv
from django.core.management.base import BaseCommand
from rides.models import User


class Command(BaseCommand):
    help = "Load users from a CSV file"

    def handle(self, *args, **kwargs):
        with open("users.csv", "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if not User.objects.filter(username=row["email"]).exists():
                    user = User(
                        role=row["role"],
                        first_name=row["first_name"],
                        last_name=row["last_name"],
                        username=f"{row['first_name']}_{row['last_name']}",
                        email=row["email"],
                        phone_number=row["phone_number"],
                    )
                    if row["role"] == "admin":
                        user.is_staff = True
                        user.is_superuser = True
                    user.set_password("1234")
                    user.save()
        self.stdout.write(self.style.SUCCESS("Successfully loaded users"))
