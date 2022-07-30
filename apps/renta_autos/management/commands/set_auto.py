import os
import json


from django.db import transaction
from django.conf import settings
from django.core.management.base import BaseCommand


from apps.renta_autos.models import Auto, AutoModelo, AutoColor, AutoTipo


BASE_DIR = settings.BASE_DIR

autos_db_json = os.path.join(BASE_DIR, 'sample_db/autos_db.json')


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open(autos_db_json, 'r') as f_obj:
            data = json.load(f_obj)

        with transaction.atomic():
            for name in list(set(data)):

                a = Auto(
                    auto_name=name,
                    modelo=AutoModelo.random_obj.random(),
                    color=AutoColor.random_obj.random(),
                    tipo=AutoTipo.random_obj.random(),
                )
                a.save()
        print("Done!")