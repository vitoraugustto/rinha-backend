import json
import os

from django.core.management.base import BaseCommand

from fighters.models import Occupation


class Command(BaseCommand):
    help = "Creates predefined occupations in the database."

    def handle(self, *args, **options):
        file_path = os.path.join(os.path.dirname(__file__), "occupations.json")

        with open(file_path, "r", encoding="utf-8") as f:
            occupations = json.load(f)

        for occupation in occupations:
            name = occupation["name"]

            if not Occupation.objects.filter(name=name).exists():
                Occupation.objects.create(**occupation)
                self.stdout.write(
                    self.style.SUCCESS(f'Occupation "{name}" created successfully')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Occupation "{name}" already exists')
                )
