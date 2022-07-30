from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required

from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db import transaction
from django.contrib import messages

from utils.utils import get_secure_nro_cta_mode


from .forms import ClientRentAutoFilterForm, ClienteRentAutoEditForm
from .models import Cliente




class RentaAutosClientsListSectionView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
	template_name = 'renta_autos/list.html'
	permission_required = (
		'renta_autos.view_cliente',
	)

	def dispatch(self, *args, **kwargs):
		user = self.request.user

		permissions = [
			'renta_autos.view_cliente',

		]

		if not user.has_perms(permissions):
			messages.warning(self.request, "No cuenta con los permisos necesarios para entrar a esta sección")
			return redirect("renta_autos:renta_autos_module")
		return super(RentaAutosClientsListSectionView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		ctx =  super().get_context_data(**kwargs)

		ctx['section_name'] = 'renta_autos'
		ctx['filter_form'] = ClientRentAutoFilterForm()
		return ctx


class RentaAutosClientsAuditoriaListView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
	template_name = 'renta_autos/clientes/auditoria.html'
	permission_required = (
		'renta_autos.view_historicalcliente',
	)

	def dispatch(self, *args, **kwargs):
		user = self.request.user

		if not user.has_perm('renta_autos.view_historicalcliente'):
			messages.warning(self.request, "No cuenta con los permisos necesarios para entrar a esta sección")
			return redirect("renta_autos:renta_autos_module")
		return super(RentaAutosClientsAuditoriaListView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		ctx =  super().get_context_data(**kwargs)
		ctx['section_name'] = 'auditoria'

		return ctx


class RentaAutosModulesSectionView(LoginRequiredMixin, TemplateView):
	template_name = 'base/module.html'


	def get_context_data(self, **kwargs):
		ctx =  super().get_context_data(**kwargs)
		ctx['module_name'] = 'Renta de Autos'
		ctx['client_list_url'] = reverse('renta_autos:renta_autos_clients_list')
		ctx['auditoria_url'] = reverse('renta_autos:renta_autos_clients_auditoria_list')
		ctx['section_name'] = 'renta_autos'

		return ctx


class RentaAutoClienteEditView(PermissionRequiredMixin, LoginRequiredMixin, View):
	form_class = ClienteRentAutoEditForm
	permission_required = (
		'renta_autos.change_cliente',
		'renta_autos.delete_cliente',
	)

	def dispatch(self, *args, **kwargs):
		user = self.request.user

		permissions = [
			'renta_autos.view_cliente',
			'renta_autos.change_cliente',
			'renta_autos.delete_cliente',
		]

		if not user.has_perms(permissions):
			return JsonResponse({
				"status": 403,
				"message": "No cuenta con los permisos necesarios para realizar esta acción.",
				"errors": "PermissionDenied",
			})
		return super(RentaAutoClienteEditView, self).dispatch(*args, **kwargs)

	def get(self, *args, **kwargs):
		uuid = self.kwargs.get('uuid', None)

		if uuid:
			instance = get_object_or_404(Cliente, id_uuid=uuid)
			form = self.form_class(instance=instance)
			ctx = {
				"form": form,
				"cli": instance,
				"rentas": instance.rentas.select_related('auto', 'cliente'),
				"nro_cta": get_secure_nro_cta_mode(instance.cuenta_numero)
			}

			return JsonResponse({
				"status": 200,
				"message": "",
				"errors": "",
				"html_content": render_to_string('renta_autos/clientes/edit_form.html', ctx, request=self.request)
			})
		else:
			return JsonResponse({
				"status": 404,
				"errors": "No se ha encontrado el respectivo ID de este registro."
			})

	def post(self, *args, **kwargs):
		data = dict()
		uuid = self.kwargs.get('uuid', None)

		try:
			if uuid:
				instance = get_object_or_404(Cliente, id_uuid=uuid)

				form = self.form_class(self.request.POST, instance=instance)

				if form.is_valid():
					instance = form.save(commit=False)
					instance.changed_by = self.request.user
					instance.save()

					data['status'] = 200
					data['id'] = instance.id_uuid
					data['message'] = "Cliente editado exitosamente."
					return JsonResponse(data)
				else:
					return JsonResponse({
						"status": 400,
						"errors": [form.errors.as_json()],
						"message": "Problemas en el procesado del formulario."
					})

		except Exception as e:
			return JsonResponse({
				"status": 500,
				"errors": str(e),
				"message": "Há ocurrido un error interno, comuniquese con el desarrollador."
			})

@login_required
def renta_auto_cliente_delete(request, uuid):
	if request.method == 'POST':
		user = request.user

		permissions = [
			'renta_autos.view_cliente',
			'renta_autos.change_cliente',
			'renta_autos.delete_cliente',
		]

		if not user.has_perms(permissions):
			return JsonResponse({
				"status": 403,
				"message": "No cuenta con los permisos necesarios para realizar esta acción.",
				"errors": "PermissionDenied",
			})


		data = dict()
		with transaction.atomic():
			try:
				instance = get_object_or_404(Cliente, id_uuid=uuid)
				instance.changed_by = request.user
				instance.delete()
				data["status"] = 202
				data["message"] = "Cliente eliminado exitosamente."
				data["errors"] = ""
				return JsonResponse(data)
			except Exception as e:
				return JsonResponse({
					'status': 500,
					'error': str(e)
				})
	return JsonResponse({
		"status": 405,
		"error": "Invalid Method"
	})