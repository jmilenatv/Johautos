from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import ( Cliente, Auto, Renta, 
AutoModelo, AutoTipo, AutoColor )



# @admin.register(Cliente, SimpleHistoryAdmin)
# class RentaAutosClienteAdmin(admin.ModelAdmin):
# 	list_display = [
# 		'cuenta_numero', 
# 		'user_name', 
# 		'fec_alta', 
# 	]
# 	search_fields = ['cuenta_numero']

admin.site.register(Auto)
admin.site.register(Renta)
admin.site.register(AutoModelo)
admin.site.register(AutoTipo)
admin.site.register(AutoColor)
admin.site.register(Cliente, SimpleHistoryAdmin)


