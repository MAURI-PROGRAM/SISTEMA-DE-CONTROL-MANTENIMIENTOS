from django.shortcuts import render
from django.http import HttpResponse
from .models import Registro_mantenimiento,Mantenimiento_Pieza,Empleados
from django.db import connection
from django.core.mail import send_mass_mail


def index(request):
    return render(request,'mant/equipos_list.html')

def envios(request):
    if request.method=='POST':
        ms1='<p>This is an <strong>important</strong> message.</p>'
        message1 = ('MANTENIMIENTOS POR REALIZAR EL DIA DE HOY', 'PRIMER AVISO', '', ['merchan.ber.mau@gmail.com'])
        message2 = ('MANTENIMIENTOS POR REALIZAR EL DIA DE HOY', 'SEGUNDO AVISO', '', ['merchan.ber.mau@gmail.com'])
        send_mass_mail((message1, message2),fail_silently=False)
        return render(request,'mant/enviar.html')

def mantenimientos_urg(request):

    consulta="""SELECT 
    a.id,
    a.codigo_mantpiz as codigo,
    b.nombre_equipo as nombre,
    b.codigo_equipo as codequi,
    a.fech_prox_mt as fecha,
    a.id as idp
FROM
    mantenimiento.control_mantenimiento_pieza as a,
    mantenimiento.control_equipo_pieza as b
WHERE
   a.notificar_mt = 1
        AND a.fech_prox_mt <= DATE_ADD(CURDATE(), INTERVAL 1 DAY)
        AND a.pieza_mt_id = b.id;"""
    mantenimiento =Mantenimiento_Pieza.objects.raw(consulta)
    consulta2="""
        SELECT id,
        name_emp,
        email_emp
        FROM mantenimiento.control_empleados;
    """
    empleado=Empleados.objects.raw(consulta2)
    contexto={'mantenimientos':mantenimiento,'empleados':empleado}
    contexto2={'empleado':empleado}
    return render(request,'mant/distribuir.html',contexto)


def dato(request):

	consulta="""SELECT 
    reg.id,COUNT(*) as numero,
    ROUND(SUM(TIMESTAMPDIFF(MINUTE,
        fech_ini_rmt,
        fech_fin_rmt) / 60), 2) AS TIEMPO_FALLO,
	
    
    TIMESTAMPDIFF(HOUR,
        MIN(fech_ini_rmt),
        MAX(fech_fin_rmt)) AS TIEMPO_TOTAL,
        
    ROUND((TIMESTAMPDIFF(HOUR,
        MIN(fech_ini_rmt),
        MAX(fech_fin_rmt))-  (ROUND(SUM(TIMESTAMPDIFF(MINUTE,
        fech_ini_rmt,
        fech_fin_rmt) / 60), 2)))/TIMESTAMPDIFF(HOUR,
        MIN(fech_ini_rmt),
        MAX(fech_fin_rmt))*100,2)  AS DISPONIBILIDAD, 
        
	ROUND((TIMESTAMPDIFF(HOUR,
        MIN(fech_ini_rmt),
        MAX(fech_fin_rmt))-  (ROUND(SUM(TIMESTAMPDIFF(MINUTE,
        fech_ini_rmt,
        fech_fin_rmt) / 60), 2)))/COUNT(*),2)  AS FIABILIDAD,
        
	ROUND(ROUND(SUM(TIMESTAMPDIFF(MINUTE,
        fech_ini_rmt,
        fech_fin_rmt) / 60), 2)/COUNT(*),2)  AS MANTENIBILIDAD,
        
        
    (SELECT 
            CASE tipo_eq
                    WHEN
                        'EQ'
                    THEN
                        (SELECT 
                                b.codigo_equipo
                            FROM
                                control_equipo_pieza AS b
                            WHERE
                                b.id = a.id)
                    WHEN
                        'pz'
                    THEN
                        (SELECT 
                                b.codigo_equipo
                            FROM
                                control_equipo_pieza AS b
                            WHERE
                                b.id = a.padre_eq_id)
                END AS EQUIPO
        FROM
            control_equipo_pieza AS a
        WHERE
            a.id = mt_pz.pieza_mt_id) AS codigo
FROM
    control_registro_mantenimiento AS reg,
    control_mantenimiento_pieza AS mt_pz
WHERE
    reg.pieza_mantenimiento_id = mt_pz.id
    AND tipo_rmt='CRT'
GROUP BY codigo
ORDER BY MANTENIBILIDAD,codigo;"""
	equipo =Registro_mantenimiento.objects.raw(consulta)
	contexto={'equipos':equipo}
	return render(request,'mant/equipos_list.html',contexto)