import MySQLdb
from datetime import date

db = MySQLdb.connect(host="localhost",    # tu host, usualmente localhost
                     user="root",         # tu usuario
                     passwd="",  # tu password
                     db="mantenimiento")        # el nombre de la base de datos

# Debes crear un objeto Cursor. Te permitirá
# ejecutar todos los queries que necesitas
cur = db.cursor()

# Usa todas las sentencias SQL que quieras
cur.execute("""SELECT 
    codigo_mantpiz,
    mantenimiento.control_equipo_pieza.nombre_equipo,
    mantenimiento.control_equipo_pieza.codigo_equipo,
    fech_prox_mt, '%Y-%m-%d'
FROM
    mantenimiento.control_mantenimiento_pieza,
    mantenimiento.control_equipo_pieza
WHERE
    notificar_mt = 1
        AND DATE_FORMAT(fech_prox_mt, '%Y-%m-%d') <= CURDATE()
        AND pieza_mt_id = mantenimiento.control_equipo_pieza.id;""")

resultados = cur.fetchall()
hoy=''
ur=''
try:
	for registro in resultados:
		if registro[3].date()<date.today():
			urg=urg+'<tr bgcolor=#F79F81"><td>'+registro[0]+'</td></td>'+registro[1]+'</td></td>'+registro[2]+'</td></tr>'
		else:
			hoy=hoy+'<tr bgcolor=#CEF6F5><td>'+registro[0]+'</td></td>'+registro[1]+'</td></td>'+registro[2]+'</td></tr>'
except Exception as e:
	raise e

hoy='<table><tr bgcolor=#FF4000"><td>CODIGO DE MANTENIMIENTO</td></td>CODIGO PIEZA</td></td>NOMBRE PIEZA</td></tr>'+hoy+'</table>'
hoy='<table><tr bgcolor=#01A9DB"><td>CODIGO DE MANTENIMIENTO</td></td>CODIGO PIEZA</td></td>NOMBRE PIEZA</td></tr>'+hoy+'</table>'