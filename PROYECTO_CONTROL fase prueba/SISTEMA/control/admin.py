from django.contrib import admin
from .models import Equipo_pieza,Mantenimiento,Mantenimiento_Pieza,Empleados,Registro_mantenimiento
# Register your models here.
# admin.site.register(Equipo_pieza)
# admin.site.register(Mantenimiento)
# admin.site.register(Mantenimiento_Pieza)
# admin.site.register(Empleados)
# admin.site.register(Registro_mantenimiento)


class Mantenimiento_PiezaInline(admin.TabularInline):
    model = Mantenimiento_Pieza
    classes = ['collapse']
    extra = 1


class Registro_mantenimientoInline(admin.TabularInline):
    model = Registro_mantenimiento
    extra = 1
    classes = ['collapse']


class Equipo_piezaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['codigo_equipo','nombre_equipo','tipo_eq','padre_eq']}),
        ('Date information', {'fields': ['date_eq'], 'classes': ['collapse']}),
    ]
    inlines = [Mantenimiento_PiezaInline]
    list_display = ('codigo_equipo','nombre_equipo', 'tipo_eq','padre_eq')
    search_fields = ['codigo_equipo']
    readonly_fields = ('date_eq',)
    list_per_page=10
    list_filter=('tipo_eq',)



class MantenimientoAdmin(admin.ModelAdmin):
    model=Mantenimiento
    fieldsets = [
        (None,               {'fields': ['codigo_mant','nombre_mant','actividad_mant']}),
        ('Date information', {'fields': ['padre_mant'], 'classes': ['collapse']}),
    ]
    # inlines = [Mantenimiento_PiezaInline]
    list_display = ['codigo_mant','nombre_mant','actividad_mant','padre_mant',]
    search_fields = ['codigo_mant']
    list_per_page=10
    list_filter=('actividad_mant','padre_mant',)

class Mantenimiento_Pieza_Admin(admin.ModelAdmin):
    model=Mantenimiento
    fieldsets = [
        (None,               {'fields': ['codigo_mantpiz','pieza_mt','mantenimiento_mt','frecuencia_mt','fech_prox_mt','notificar_mt']}),
    ]
    inlines = [Registro_mantenimientoInline]
    readonly_fields = ('codigo_mantpiz','pieza_mt','mantenimiento_mt','frecuencia_mt','fech_prox_mt','notificar_mt',)
    #Registro_mantenimientoInline.can_delete=False
    Mantenimiento_PiezaInline.can_delete=False
    list_display = ['pieza_mt','mantenimiento_mt','codigo_mantpiz']
    search_fields = ['codigo_mantpiz']
    list_per_page=10



class Registro_mantenimientoAdmin(admin.ModelAdmin):
    model=Registro_mantenimiento
    fieldsets = [
        (None,               {'fields': ['pieza_mantenimiento','tipo_rmt','fech_ini_rmt','fech_fin_rmt','observacion_rmt']}),
        ('Date information', {'fields': ['encargados_rmt','defecto_rmt','costo_rmt'], 'classes': ['collapse']}),
    ]
    # inlines = [Mantenimiento_PiezaInline]
    list_display = ('pieza_mantenimiento','fech_ini_rmt','duracion','FECHA_PROXIMO')
    search_fields = ['pieza_mantenimiento']
    list_filter=('fech_ini_rmt',)
    list_per_page=10




admin.site.register(Mantenimiento,MantenimientoAdmin)
admin.site.register(Equipo_pieza, Equipo_piezaAdmin)
admin.site.register(Registro_mantenimiento,Registro_mantenimientoAdmin)
admin.site.register(Mantenimiento_Pieza,Mantenimiento_Pieza_Admin)
admin.site.register(Empleados)