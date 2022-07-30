from django.db import transaction
from django.conf import settings
from django.core.management.base import BaseCommand


from apps.renta_autos.models import Auto, Cliente, Renta


BASE_DIR = settings.BASE_DIR



class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        with transaction.atomic():
            for cli in Cliente.objects.all():

                r = Renta(
                    auto=Auto.random_obj.random(),
                    cliente=cli
                )
                r.save()
        print("Done!")