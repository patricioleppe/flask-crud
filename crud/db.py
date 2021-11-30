# importamos para la conexion 
# de la BD.  pip install mysql-connector-python
import mysql.connector

# click lo ocuparemos para 
# poder ejecutar comandos
# en la terminal asi
# crear tablas modificarlas etc.
import click

# current_app: mantiene la 
# aplicacion que estamos ejecutando
#
# g   es una variable para asignarle
# distintas variables asi poder acceder
# aca almacenaremos el usuario.
from flask import current_app, g

# esto sirve para obtener la 
# configuracion de las conexiones de
# base de datos de la app.
from flask.cli import with_appcontext

# importamos archivo llamado
# schema este contiene todos los
# scripts que necesitamos para 
# poder crear la Base de Datos.
from .schema import instructions

#Funcion para obeter la conexion 
# y el curor de la BD
def get_db():
    # no existe la conexion en g 
    if 'db' not in g:
        # se crea una nueva 
        # propiedad dentro de g.
        g.db = mysql.connector.connect(
            host = current_app.config['DATABASE_HOST'],
            user = current_app.config['DATABASE_USER'],
            password = current_app.config['DATABASE_PASSWORD'],
            database = current_app.config['DATABASE'],
        )

        # acceder a las propiedades 
        # como un diccionario de datos
        # a cursor se le pasa dictionary=True.
        g.c  = g.db.cursor(dictionary=True)
    
    # de esta manera al llamar a get_db()
    # obtendremos la base de datos g.db
    # y tambien el cursor g.c.
    return g.db, g.c

# Funcion que cierre la conexion
# a la base de datos cada vez que 
# hagamos una peticion, asi la conexion
# queda cerrada y flask la cierre.
def close_db(e=None):
    # Quitar la propiedad de 
    # db a g.
    db = g.pop('db', None)
    
    #si db no esta definido
    # Significa que nunca llamamos a 
    # get_db() ,  por lo tanto no hace nada 
    # pero si esta definido la cerramos con 
    # db.close() .
    if db is not None:
        db.close()

#definir init_db()
def init_db():  
    # importar la base 
    # y el cursor utiliando
    # solo una linea.
    db, c = get_db()
    # como hay que pasar las 
    # instrucciones de sql linea por linea
    # lo mejor es iterarlas todas
    for i in instructions:
        c.execute(i)

    db.commit()


# init-db es un nombre que le 
# pasaremos nosotros, # nos servira 
# cuando quieramos llamarlo en la 
# terminal 
# En la terminal seria:
# flask init-db
# y eso ejecutaria esta funcion: 
@click.command('init-db')

# ! para que script se ejecute 
# con EXITO hay que indicar que 
# utilice el contexto de la aplicacion 
# para que pueda acceder a las 
# variables de configuracion ESTAS : 
# g.db=mysql.connector.connect(...) 
@with_appcontext

# Script que ejecutara un set 
# de instrucciones que 
# escribiremos en SQL
# nos permitira crear tablas 
# para almacenar datos 
# de nuestra aapliacion
def init_db_command():
    init_db()
    # Esto indica que el el script
    # a teneminado de correr 
    # con exito
    click.echo('Base de datos inicializada')

# funcion donde se pasa argumento app
# que creamos en el archivo __init__.py 
# ahi agregar la func. cuando estemos 
# terminando la peticion.
def init_app(app):
    # cuando termine de realizar la 
    # peticion a FLASK haremos esto:
    # y cerrara la conexion a la bd.
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)