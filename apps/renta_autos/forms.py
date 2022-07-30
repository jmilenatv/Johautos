from pyexpat import model
from django import forms

from .models import (
	Auto, AutoColor, AutoModelo, AutoTipo, Cliente
)





class ClienteRentAutoEditForm(forms.ModelForm):

	fec_birthday = forms.DateField(
		widget=forms.DateInput(
			attrs={'class': 'form-control form-control-sm', 'type': 'date'},
			format=('%Y-%m-%d') ),
		label="Fecha de Nacimiento:",
		required=False,
		)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for form in self.visible_fields():
			form.field.widget.attrs['class'] = 'form-control form-control-sm mb-3'

	class Meta:
		model = Cliente
		fields = (
			"codigo_zip",
			"color_favorito",
			"fec_birthday",
		)
	


class ClientRentAutoFilterForm(forms.Form):

	color_choices = forms.ModelMultipleChoiceField(
		queryset=AutoColor.objects.all(), 
		required=False,
		widget=forms.CheckboxSelectMultiple(
			attrs={
				'class': 'form-control mb-3 form-filter-input'}))

	auto_choices = forms.ModelMultipleChoiceField(
			queryset=Auto.objects.all(), 
			required=False,
			widget=forms.CheckboxSelectMultiple(
				attrs={
					'class': 'form-control mb-3 form-filter-input'}))

	auto_modelo_choices = forms.ModelMultipleChoiceField(
		queryset=AutoModelo.objects.all(), 
		required=False,
		widget=forms.CheckboxSelectMultiple(
			attrs={
				'class': 'form-control mb-3 form-filter-input'}))

	auto_tipo_choices = forms.ModelMultipleChoiceField(
		queryset=AutoTipo.objects.all(), 
		required=False,
		widget=forms.CheckboxSelectMultiple(
			attrs={
				'class': 'form-control mb-3 form-filter-input'}))

	fec_alta = forms.DateField(
		widget=forms.DateInput(
			attrs={'class': 'form-control form-control-sm'}), 
			label="Fecha de alta:",
			required=False,
			)

	min_compras_realizadas = forms.IntegerField(
		widget=forms.NumberInput(
			attrs={'class': 'form-control form-control-sm form-filter-input mb-3', 'min':'0', 'max': '100'}))

	max_compras_realizadas = forms.IntegerField(
		widget=forms.NumberInput(
			attrs={'class': 'form-control form-control-sm form-filter-input mb-3', 'min':'0', 'max': '100'}))