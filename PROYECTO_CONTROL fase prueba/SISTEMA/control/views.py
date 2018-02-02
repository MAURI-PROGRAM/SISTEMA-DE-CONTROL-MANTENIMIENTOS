from django.shortcuts import render
from django.http import HttpResponse
from .models import Registro_mantenimiento
from django.db import connection


def index(request):
    return render(request,'mant/equipos_list.html')

    

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