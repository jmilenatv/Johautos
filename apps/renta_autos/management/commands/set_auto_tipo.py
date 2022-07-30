import os
import random
import json


from django.db import transaction
from django.conf import settings
from django.core.management.base import BaseCommand


from apps.renta_autos.models import AutoTipo


BASE_DIR = settings.BASE_DIR

autos_tipo_db_json = os.path.join(BASE_DIR, 'sample_db/autos_tipo_db.json')


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open(autos_tipo_db_json, 'r') as f_obj:
            data = json.load(f_obj)

        with transaction.atomic():
            for tipo in list(set(data)):
                t = AutoTipo(
                    tipo=tipo
                )
                t.save()
        print("Done!")