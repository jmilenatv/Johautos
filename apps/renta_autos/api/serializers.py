import os
from rest_framework import serializers
from django.conf import settings

from apps.renta_autos.models import Renta, Cliente, Auto

from utils.utils import get_secure_nro_cta_mode





class AuditClienteRentaAutoSerializer(serializers.ModelSerializer):

	class Meta:
		model = Cliente
		fields = (
			"user_name",
		)

	def to_representation(self, instance):
		rep = super(AuditClienteRentaAutoSerializer, self).to_representation(instance)

		rep['user_name'] = f"{get_secure_nro_cta_mode(instance.cuenta_numero)} - {rep['user_name'] }"
		rep['history_date'] = instance.history_date
		rep['history_change_reason'] = instance.history_change_reason
		rep['changed_by'] = instance.changed_by.username

		return rep


class AutoSerializer(serializers.ModelSerializer):

	class Meta:
		model = Auto
		fields =  (
			"auto_name",
			"modelo",
			"tipo",
			"color",
		)

	def to_representation(self, instance):
		rep = super(AutoSerializer, self).to_representation(instance)

		rep['modelo'] = instance.modelo.modelo
		rep['tipo'] = instance.tipo.tipo
		rep['color'] = instance.color.color

		return rep


class ListRentaAutoSerializer(serializers.ModelSerializer):
	auto = AutoSerializer(read_only=True)

	class Meta:
		model = Renta
		fields = (
			'auto',
		)


class ClienteDetailSerializer(serializers.ModelSerializer):
	rentas = ListRentaAutoSerializer(many=True, read_only=True)

	class Meta:
		model = Cliente
		fields = (
			"cuenta_numero",
			"color_favorito",
			"fec_birthday",
			"fec_alta",
			"rentas",
			"user_name",
			"codigo_zip",
			"id_uuid",
		)

	def to_representation(self, instance):
		rep = super(ClienteDetailSerializer, self).to_representation(instance)
		rep['cuenta_numero'] = get_secure_nro_cta_mode(rep['cuenta_numero'])
		rep['avatar'] = os.path.join(settings.STATIC_URL, 'src/img/user_no_profile.png')
		rep['foto_dni'] = os.path.join(settings.STATIC_URL, 'src/img/dni_black.png')

		return rep


class ClienteRentaAutoSerializer(serializers.ModelSerializer):
	rentas = ListRentaAutoSerializer(many=True, read_only=True)


	class Meta:
		model = Cliente
		fields = (
			"fec_alta",
			"user_name",
			"codigo_zip",
			"cuenta_numero",
			"color_favorito",
			"fec_birthday",
			"rentas",
			"compras_realizadas",
			"id_uuid",
		)

	def to_representation(self, instance):
		rep = super(ClienteRentaAutoSerializer, self).to_representation(instance)

		rep['cuenta_numero'] = get_secure_nro_cta_mode(rep['cuenta_numero']) 
		rep['fec_alta'] = instance.fec_alta.strftime('%d/%m/%Y, %H:%M:%S')

		return rep