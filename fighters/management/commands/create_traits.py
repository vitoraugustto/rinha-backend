import json
import os

from django.core.management.base import BaseCommand

from fighters.models import Trait


class Command(BaseCommand):
    help = "Creates predefined traits in the database."

    def handle(self, *args, **options):
        file_path = os.path.join(os.path.dirname(__file__), "traits.json")

        with open(file_path, "r", encoding="utf-8") as f:
            traits = json.load(f)

        for trait in traits:
            name = trait["name"]

            if not Trait.objects.filter(name=name).exists():
                Trait.objects.create(**trait)
                self.stdout.write(
                    self.style.SUCCESS(f'Trait "{name}" created successfully')
                )
            else:
                self.stdout.write(self.style.WARNING(f'Trait "{name}" already exists'))
