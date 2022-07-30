from django.db import transaction
from django.core.management.base import BaseCommand


from apps.renta_autos.models import Auto, Cliente, Renta



class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        i = 0
        with transaction.atomic():
            while i <= 65:
                r = Renta(
                    auto=Auto.random_obj.random(),
                    cliente=Cliente.random_obj.random()
                )
                r.save()
                i += 1
        print("Done!")