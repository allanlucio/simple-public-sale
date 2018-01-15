from django.contrib import admin
from .models import *

class CaracteristicaPrendaInline(admin.TabularInline):
    model=CaracteristicaPrenda
    extra = 2
    max_num = 3

class PrendaAdmin(admin.ModelAdmin):
    inlines = (CaracteristicaPrendaInline,)

admin.site.register(Evento)
admin.site.register(Prenda,PrendaAdmin)
admin.site.register(Movimento)
# admin.site.register(Doador)
admin.site.register(TipoPrenda)
admin.site.register(Participante)
admin.site.register(Caracteristica)
admin.site.register(CaracteristicaPrenda)

