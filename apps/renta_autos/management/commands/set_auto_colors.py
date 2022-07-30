import os
import ast


from django.db import transaction
from django.conf import settings
from django.core.management.base import BaseCommand


from apps.renta_autos.models import AutoColor


BASE_DIR = settings.BASE_DIR

auto_color_db_path = os.path.join(BASE_DIR, 'sample_db/autos_color_db.txt')


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open(auto_color_db_path, 'r') as f:
            color_tuple = ast.literal_eval(f.read())

        with transaction.atomic():
            for color in color_tuple:
                c = AutoColor(
                    color=color
                )
                c.save()
        print("Done!")