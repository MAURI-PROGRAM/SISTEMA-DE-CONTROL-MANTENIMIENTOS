from django.db import models
from django.utils import timezone
from datetime import datetime,timedelta
from django.utils.timezone import now

class Equipo_pieza(models.Model):
	codigo_equipo = models.CharField(max_length=12,unique=True,help_text="",verbose_name='Código')
	nombre_equipo = models.CharField(max_length=50,verbose_name='Nombre')
	tipo_eq = models.CharField(max_length=2,choices=(('PZ', 'Pieza'),('EQ', 'Equipo'),),verbose_name='Tipo')
	date_eq = models.DateTimeField(default=timezone.now,verbose_name='Fecha de registro')
	padre_eq = models.ForeignKey('self', on_delete=models.CASCADE,null=True,default='null',blank=True,verbose_name='Código del equipo')
	def __str__(self):
		return (self.codigo_equipo)
	class Meta:
		verbose_name_plural = 'EQUIPOS Y PIEZAS'
		ordering = ['codigo_equipo']

class Mantenimiento(models.Model):
	codigo_mant = models.CharField(max_length=15,help_text="",unique=True,verbose_name='Código del mantenimiento' )
	nombre_mant = models.CharField(max_length=50,help_text="",verbose_name='Nombre del mantenimiento')
	actividad_mant = models.CharField(max_length=200,help_text="",verbose_name='Descripción del mantenimiento')
	padre_mant = models.ForeignKey('self', on_delete=models.CASCADE,null=True,default='null',blank=True,verbose_name='Tipo de mantenimiento ')
	def __str__(self):
		return (self.codigo_mant)
	class Meta:
		verbose_name_plural = 'TIPOS DE MANTENIMIENTOS'

class Mantenimiento_Pieza(models.Model):
	codigo_mantpiz = models.CharField(max_length=17,help_text="",unique=True,verbose_name='Código para el mantenimiento del eq/pz' )
	pieza_mt = models.ForeignKey(Equipo_pieza, on_delete=models.CASCADE,verbose_name='código del equipo/pieza')
	mantenimiento_mt = models.ForeignKey(Mantenimiento, on_delete=models.CASCADE, verbose_name='Código del mantenimiento')
	frecuencia_mt= models.PositiveSmallIntegerField(default=0,verbose_name='Periodicidad(H)')
	fech_prox_mt = models.DateTimeField(default=datetime.now(),verbose_name='Fecha del próximo mantenimiento')
	notificar_mt = models.BooleanField(default=True,verbose_name='Notificar mantenimiento')
	def __str__(self):
		return (self.codigo_mantpiz)
	class Meta:
		verbose_name_plural = 'MANTENIMIENTOS DE EQUIPOS Y PIEZAS'
	def save(self):
	 	if  self.frecuencia_mt>0:
	 		horas=self.frecuencia_mt
	 		fechaprox=datetime.now()+timedelta(hours=horas)		
	 	else:
	 		fechaprox=datetime.now()
	 	self.fech_prox_mt=fechaprox
	 	super(Mantenimiento_Pieza,self).save()

class Empleados(models.Model):
    name_emp = models.CharField(max_length=200,verbose_name='Nombre del empleado')
    email_emp = models.EmailField(verbose_name='Correo del empleado')
    cargo_emp= models.CharField(max_length=200, verbose_name='Cargo del empleado')
    def __str__(self):
        return self.name_emp
    class Meta:
    	verbose_name_plural = 'EMPLEADOS'

class Registro_mantenimiento(models.Model):
	pieza_mantenimiento = models.ForeignKey(Mantenimiento_Pieza, on_delete=models.CASCADE)
	tipo_rmt = models.CharField(max_length=3,choices=(('CRT', 'Correctivo'),('PRV', 'Preventivo'),))
	fech_ini_rmt = models.DateTimeField('fecha de inicio',default=timezone.now)
	fech_fin_rmt = models.DateTimeField('fecha de finalizacion',default=timezone.now)
	observacion_rmt = models.CharField(max_length=100,help_text="")
	encargados_rmt = models.ManyToManyField(Empleados,blank=True)
	defecto_rmt=models.CharField(max_length=25,help_text="")
	costo_rmt=models.DecimalField(default=0.0, max_digits=6, decimal_places=2)
	def duracion(self):
		dif=self.fech_fin_rmt-self.fech_ini_rmt
		return dif.total_seconds()//3600
	class Meta:
		verbose_name_plural = 'REGISTRO DE MANTENIMIENTOS'
	def FECHA_PROXIMO(self):
		if  self.pieza_mantenimiento.frecuencia_mt>0:
			horas=self.pieza_mantenimiento.frecuencia_mt
			fechaprox=datetime.now()+timedelta(hours=horas)
			self.pieza_mantenimiento.fech_prox_mt=fechaprox
		else:
			fechaprox=datetime.now()
		return str(self.pieza_mantenimiento.fech_prox_mt)
	# def save(self):
	# 	if  self.pieza_mantenimiento.frecuencia_mt>0:
	# 		horas=self.pieza_mantenimiento.frecuencia_mt
	# 		fechaprox=datetime.now()+timedelta(hours=horas)
			
	# 	else:
	# 		fechaprox=datetime.now()
	# 	self.pieza_mantenimiento.fech_prox_mt=fechaprox
	# 	super(Registro_mantenimiento,self).save()