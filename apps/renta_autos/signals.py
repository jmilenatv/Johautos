from .models import (
    Renta, Cliente
)

from django.db import transaction
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from simple_history.utils import update_change_reason


# Control the flow of save 
# transaction in DB.
def on_transaction_commit(func):
   def inner(*args, **kwargs):
      transaction.on_commit(lambda: func(*args, **kwargs))

   return inner



@on_transaction_commit
@receiver(post_save, sender=Renta)
def save_compra_realizada_to_cliente(sender, instance, created, **kwargs):

   cliente = instance.cliente
   cliente.compras_realizadas = cliente.rentas.count()
   cliente.save()



@on_transaction_commit
@receiver(post_save, sender=Cliente)
def add_post_save_reason_to_history_for_auditory(sender, instance, created, **kwargs):

   if created:
      update_change_reason(instance, "Registro Creado")
   else:
      update_change_reason(instance, "Registro editado.")



@on_transaction_commit
@receiver(post_delete, sender=Cliente)
def add_post_delete_reason_to_history_for_auditory(sender, instance, **kwargs):

   update_change_reason(instance, "Registro Eliminado")