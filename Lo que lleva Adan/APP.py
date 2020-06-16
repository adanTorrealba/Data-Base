

#Importando librerias
from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from flask_mysqldb import MySQL
import bcrypt

#Creando el objeto flask
app = Flask(__name__)

#Estableciendo la llave secreta
app.secret_key = "mySecretKey"

#Configurando la conexion con la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'tintoreriaelegante'

#Creando el objeto mysql
mysql = MySQL(app)

#Semilla para encriptamiento
semilla = bcrypt.gensalt()

#Definiendo la ruta principal
@app.route("/")

#Funcion principal
def main():

 if 'nombre' in session:
     #Cargar pag principal
     return render_template('inicio.html')
 else:
     #Cargar pag login
     return render_template('ingresar.html')

#Definiendo la ruta del index
@app.route("/inicio")

#Funcion de inicio
def inicio():

    #Verificar si hay una sesion abierta
    if 'nombre' in session:
        #Cargar pag principal
        return render_template('inicio.html')
    else:
        #Cargar pag login
        return render_template('ingresar.html')

#Definiendo la ruta del registro
@app.route("/registro", methods = ["GET", "POST"])

#Funcion para registrar
def registro():

    #Verificar si ha entrado por el metodo get
    if (request.method == "GET"):

        #Verificar si hay una sesion abierta
        if 'nombre' in session:
            #Cargar pag principal
            return render_template('inicio.html')
        else:
            #Cargar pag login
            return render_template('ingresar.html')

    #Metodo post
    else:

        #Obtener los datos
        nombre = request.form['nmNombreRegistro']
        apellido = request.form['nmApellidoRegistro']
        correo = request.form['nmCorreoRegistro']
        password = request.form['nmPasswordRegistro']

        #Incriptando password
        password_encode = password.encode("utf-8")
        password_encriptado = bcrypt.hashpw(password_encode, semilla)

        #Prepara el query para la insercion
        sQuery = 'INSERT to login (nombre, apellido, correo, password) VALUES (%s, %s, %s, %s)'

        #crear un cursor para la ejecucion
        cur = mysql.connection.cursor()

        #Ejecutando la sentencia
        cur.execute(sQuery, (nombre, apellido, correo, password_encriptado))

        #Ejecutando el commit
        mysql.connection.commit()

        #Registrando la sesion
        session['nombre'] = nombre
        session['apellido'] = apellido
        session['correo'] = correo

        #Redirigiendo al index
        return redirect(url_for('inicio'))

#Definiendo la ruta para ingresar
@app.route("/ingresar", methods = ["GET", "POST"])

#Funcion para ingresar
def ingresar():

    #Verificar si ha entrado por el metodo get
    if (request.method == "GET"):

        #Verificar si hay una sesion abierta
        if 'nombre' in session:
            #Cargar pag principal
            return render_template('inicio.html')
        else:
            #Cargar pag login
            return render_template('ingresar.html')

    #Metodo post
    else:

        #Obteniendo los datos
        correo = request.form['nmCorreoLogin']
        password = request.form['nmPasswordLogin']
        password_encode = password.encode("utf-8")

        #Crear cursor para la ejecucion
        cur = mysql.connection.cursor()

        #Preparando el querty para la consulta
        sQuery = 'SELECT correo, password FROM login WHERE correo = %s'

        #Ejecutnado la sentencia
        cur.execute(sQuery, [correo])

        #Obeteniendo el dato
        usuario = cur.fetchone()

        #Cerrando la consulta
        cur.close()

        #Verificando si se obtuvieron los datos
        if (usuario != None):

            #Obteniendo el password encriptado encode
            password_encriptado_encode = usuario[1].encode()

            #Verificnado el password
            if (bcrypt.checkpw(password_encode, password_encriptado_encode)):

                #Registando la sesion
                session['nombre'] = usuario[2]
                session['apellido'] = usuario[3]
                session['correo'] = correo

                #Redirigiendo al index
                return redirect(url_for('inicio'))

            else:
                #Password incorrecto
                flash("El password no es correcto.", "alert-warning")

                #Redirigir a ingresar
                return render_template('ingresar.html')

        else:
            #Correo incorrecto
            flash("El correo no existe.", "alert-warning")

            #Redirigir a ingresar
            return render_template('ingresar.html')

#Definiendo la ruta de salida
@app.route("/salir")

#Funcion para salir
def salir():

    #Limpiando las secciones
    session.clear()

    #Redirigiendo a ingresar
    return redirect(url_for('ingresar'))

#Ejecutar todo
if __name__ == "__main__":

    #Ejecutando el servidor
    app.run(port = 3000, debug = True, use_reloader = False)
