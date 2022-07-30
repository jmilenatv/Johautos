from multiprocessing.spawn import is_forking
import re
from datetime import datetime


from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

from django.db import connection

from .pagination import CustomPagination


from apps.renta_autos.models import Renta, Cliente

from .serializers import (
	ClienteRentaAutoSerializer,
	ClienteDetailSerializer,
	AuditClienteRentaAutoSerializer
)




class ClienteRentaAutosListAPIView(ListAPIView):
	serializer_class = ClienteRentaAutoSerializer
	pagination_class = CustomPagination
	permission_classes = [IsAuthenticated]


	def get_queryset(self):
		queryset = self.get_filtered_queryset()

		return queryset

	def get_filtered_queryset(self):
		query = self.request.GET.get('query')
		auto_choices = self.request.GET.getlist('auto_choices')
		color_choices = self.request.GET.getlist('color_choices')
		auto_modelo_choices = self.request.GET.getlist('auto_modelo_choices')
		created = self.request.GET.get('fec_alta')
		auto_tipo_choices = self.request.GET.getlist('auto_tipo_choices')
		min_compra = self.request.GET.get('min_compras_realizadas')
		max_compra = self.request.GET.get('max_compras_realizadas')


		queryset = Cliente.objects.all()

		if query is not None and query != '':
			query = query.strip()
			if query.isnumeric():
				if len(query) >= 4:
					first_nums = query[:2]
					last_nums = query[len(query) - 2:]
					queryset = queryset.filter(
						cuenta_numero__startswith=first_nums
					)
					queryset = queryset.filter(
						cuenta_numero__endswith=last_nums
					)
			else:
				queryset = queryset.filter(Q(user_name__icontains=query)).distinct()

		if created and created != '':
			date_range = re.findall(r'(\d+-\d+-\d+)', created)
			start = tuple(date_range[0].split("-"))
			end = tuple(date_range[1].split("-"))

			queryset = queryset.filter(fec_alta__range=[
				datetime(int(start[0]), int(start[1].lstrip('0')), int(start[2])), 
				datetime(int(end[0]), int(end[1].lstrip('0')), int(end[2]))
			])

		if auto_choices and auto_choices != ['']:
			queryset = queryset.filter(
				rentas__auto__auto_name__in=auto_choices)

		if color_choices and color_choices != ['']:
			queryset = queryset.filter(
				rentas__auto__color__color__in=color_choices)

		if auto_modelo_choices and auto_modelo_choices != ['']:
			queryset = queryset.filter(
				rentas__auto__modelo__modelo__in=auto_modelo_choices)

		if auto_tipo_choices and auto_tipo_choices != ['']:
			queryset = queryset.filter(
				rentas__auto__tipo__tipo__in=auto_tipo_choices)

		if min_compra != '' or max_compra != '':
			if min_compra and max_compra:
				queryset = queryset.filter(
					compras_realizadas__gte=min_compra, compras_realizadas__lte=max_compra)
			elif min_compra:
				queryset = queryset.filter(
					compras_realizadas__gte=min_compra)
			elif max_compra:
				queryset = queryset.filter(
					compras_realizadas__lte=max_compra)

		return queryset


class RentaAutosAuditListAPIView(ListAPIView):
	serializer_class = AuditClienteRentaAutoSerializer
	pagination_class = CustomPagination
	permission_classes = [IsAuthenticated]


	def get_queryset(self):
		queryset = Cliente.history.all()

		return queryset
	


class ClienteDetailAPIView(APIView):
	serializer_class = ClienteDetailSerializer
	permission_classes = (permissions.IsAuthenticated,)


	def get(self, request, uuid):
		cli = get_object_or_404(Cliente, id_uuid=uuid)
		data = self.serializer_class(cli).data
		return Response(data)
