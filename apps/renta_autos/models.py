import uuid

from django.db import models
from mirage import fields
from django.db.models.aggregates import Count
from random import randint
from simple_history.models import HistoricalRecords


from utils.utils import get_secure_nro_cta_mode



class BaseRandomManager(models.Manager):
    # Used only to populate the db.
    def random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]


class RentaModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('auto')


class AutoModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('modelo', 'tipo', 'color')


def upload_to(instance, filename):
    return 'renta_autos/clients/{user_name}/{filename}'.format(
        user_name=instance.user_name, 
        filename=filename
    )

class Cliente(models.Model):
    id_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    fec_alta = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=150)
    codigo_zip = models.CharField(max_length=50)
    credit_card_num = fields.EncryptedCharField()
    credit_card_ccv = fields.EncryptedCharField()
    cuenta_numero = models.IntegerField()
    direccion = models.CharField(max_length=250)
    geo_latitud = models.FloatField()
    geo_longitud = models.FloatField()
    color_favorito = models.CharField(max_length=100)
    foto_dni = models.ImageField(upload_to=upload_to, blank=True, null=True)
    ip = models.CharField(max_length=15)
    avatar = models.ImageField(upload_to=upload_to, blank=True, null=True)
    fec_birthday = models.DateField()
    compras_realizadas = models.IntegerField(default=0, blank=True, null=True)
    history = HistoricalRecords()
    changed_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)


    objects = models.Manager() # The default manager.
    random_obj = BaseRandomManager()


    def __str__(self):
        return f"{get_secure_nro_cta_mode(self.cuenta_numero)} - {self.user_name}"


    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['fec_alta']
 

class AutoModelo(models.Model):
    modelo = models.CharField(max_length=100)

    objects = models.Manager() # The default manager.
    random_obj = BaseRandomManager()

    def __str__(self):
        return self.modelo


class AutoTipo(models.Model):
    tipo = models.CharField(max_length=100)

    objects = models.Manager() # The default manager.
    random_obj = BaseRandomManager()


    def __str__(self):
        return self.tipo


class AutoColor(models.Model):
    color = models.CharField(max_length=100)

    objects = models.Manager() # The default manager.
    random_obj = BaseRandomManager()


    def __str__(self):
        return self.color


class Auto(models.Model):
    auto_name = models.CharField(max_length=100)
    modelo = models.ForeignKey(AutoModelo, on_delete=models.CASCADE)
    tipo = models.ForeignKey(AutoTipo, on_delete=models.CASCADE)
    color = models.ForeignKey(AutoColor, on_delete=models.CASCADE)

    objects = AutoModelManager() # The default manager.
    random_obj = BaseRandomManager()

    
    def __str__(self):
        return self.auto_name


class Renta(models.Model):
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='rentas')

    objects = RentaModelManager()

    class Meta:
        verbose_name = 'Renta'
        verbose_name_plural = 'Rentas Realizadas'
        ordering = ['id']

    def __str__(self):
        return "Renta: {auto} - por: {cli}".format(
            auto=self.auto,
            cli=self.cliente
        )