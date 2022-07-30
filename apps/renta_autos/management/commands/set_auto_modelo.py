import os
import json


from django.db import transaction
from django.conf import settings
from django.core.management.base import BaseCommand


from apps.renta_autos.models import AutoModelo


BASE_DIR = settings.BASE_DIR

autos_modelo_db_json = os.path.join(BASE_DIR, 'sample_db/autos_modelo_db.json')


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open(autos_modelo_db_json, 'r') as f_obj:
            data = json.load(f_obj)

        with transaction.atomic():
            for model in list(set(data)):
                m = AutoModelo(
                    modelo=model
                )
                m.save()
        print("Done!")