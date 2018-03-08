import smtplib
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime,date
import MySQLdb


db = MySQLdb.connect(host="localhost",    # tu host, usualmente localhost
                     user="root",         # tu usuario
                     passwd="",  # tu password
                     db="mantenimiento")        # el nombre de la base de datos

# Usa todas las sentencias SQL que quieras
cur = db.cursor()
cur.execute("""SELECT 
    codigo_mantpiz,
    mantenimiento.control_equipo_pieza.nombre_equipo,
    mantenimiento.control_equipo_pieza.codigo_equipo,
    fech_prox_mt,
    mantenimiento.control_mantenimiento_pieza.id
FROM
    mantenimiento.control_mantenimiento_pieza,
    mantenimiento.control_equipo_pieza
WHERE
    notificar_mt = 1
        AND DATE_FORMAT(fech_prox_mt, '%Y-%m-%d') <= CURDATE()
        AND pieza_mt_id = mantenimiento.control_equipo_pieza.id;""")

resultados = cur.fetchall()
hoy=''
urg=''
try:
	for registro in resultados:
		if registro[3].date()<date.today():
			urg=urg+'<tr bgcolor=#EB984E border=2><td><A href="http://localhost:8000/admin/control/mantenimiento_pieza/'+str(registro[4])+'/change/">'+registro[0]+'</A></td></td>'+registro[1]+'</td></td>'+registro[2]+'</td></td>'+str(registro[3])+'</td></tr>'
		else:
			hoy=hoy+'<tr bgcolor=#D1F2EB border=2><td><A href="http://localhost:8000/admin/control/mantenimiento_pieza/'+str(registro[4])+'/change/">'+registro[0]+'</A></td></td>'+registro[1]+'</td></td>'+registro[2]+'</td></td>'+str(registro[3])+'</td></tr>'
except Exception as e:
	raise e

hoy='<table ><tr bgcolor="#34495E" border=2><td><FONT COLOR="FFFFFF">CODIGO DE MANTENIMIENTO</td></td><FONT COLOR="FFFFFF">NOMBRE PIEZA</td></td><FONT COLOR="FFFFFF">CODIGO PIEZA</td></td><FONT COLOR="FFFFFF">FECHA MANTENIMIENTO</td></tr>'+hoy+'</table>'
urg='<table ><tr bgcolor="#641E16" border=2><td><FONT COLOR="FFFFFF">CODIGO DE MANTENIMIENTO</td></td><FONT COLOR="FFFFFF">NOMBRE PIEZA</td></td><FONT COLOR="FFFFFF">CODIGO PIEZA</td></td><FONT COLOR="FFFFFF">FECHA MANTENIMIENTO</td></tr>'+urg+'</table>'



fecha_actual=datetime.now()

fromaddr = 'proyecto.titulacion.mant@gmail.com'
#,'daniponce1995@gmail.com','luzkristy@gmail.com','merchan.ber.mau@hotmail.com'
toaddr = ('merchan.ber.mau@gmail.com','daniponce1995@gmail.com')

mail_msg = """
<h2>TAREAS ASIGNADAS PARA EL """+fecha_actual.strftime("%d/%m/%y")+"""</h2>
<h3>CODIGOS DE MANTENIMIENTO</h3><br><h2>MANTENIMIENTOS PARA EL DIA DE HOY</h2>
<A href="http://localhost:8000/admin/control/mantenimiento_pieza/">IR A LA PAGINA</A>

<br><br>"""+hoy+"""<br><h2>MANTENIMIENTOS URG</h2><br>"""+urg+"""<br><br>
"""
message = MIMEText(mail_msg, 'html', 'utf-8')
message['From'] = Header("CONTROL DE MANTENIMIENTOS GENEROCA", 'utf-8')
message['To'] =  Header("SUPERVISORES", 'utf-8')

subject = 'MANTENIMIETOS A LA FECHA DE :'+fecha_actual.strftime("%d-%m-%y")+'.'
message['Subject'] = Header(subject, 'utf-8')
 
# Datos
username = 'proyecto.titulacion.mant@gmail.com'
password = 'proyecto19'


try:
    smtpObj = smtplib.SMTP('smtp.gmail.com:587')
    smtpObj.starttls()
    smtpObj.login(username,password)
    for envios in toaddr:
    	smtpObj.sendmail(fromaddr, envios, message.as_string())
    smtpObj.quit()
    print("ENVIADO")
except smtplib.SMTPException:
    print ("Error: NO SE PUDO ENVIAR")