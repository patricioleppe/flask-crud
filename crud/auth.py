# los modulos en flask 
# se divinen en blueprint
#
import functools
from logging import error

from flask import (
    # blueprint: congiguracion
    # flash: mensajes para que lo muestre
    # g: variable para la bd
    # reder_template: rederizar plantillas
    # request: vamos a recibir datos
    # url_for: vamos a creaer urls
    # session: para saber si el usuario 
    # esta interacautnaod con nostoros.
    Blueprint, flash, g, render_template, request, url_for, session, redirect
)
# check: verificar pass si es igual a otra
# generate: encriptar la contraseña.
from werkzeug.security import check_password_hash, generate_password_hash
#from werkzeug.utils import redirect

# get_db: interactuar con la 
# base de datos

from crud.db import get_db

#Crear nuestro primer Blueprint
#bp : nombre como el archivo auth
# url_pre: a todas las url que estan abajo
# el string se lo concatenara
# ejemplo si defino registro la url quedaria
# localhost:5000/auth/registro.
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username =  request.form['username']
        password =  request.form['password']
        password2 =  request.form['password2']
        
        if password==password2:
            db, c = get_db()
            error=None
            sql = 'select id from user where username = %s'
            # print(sql)
            c.execute(
                sql, (username,)
            )
            if not username:
                error='Username es requerido'
            if not password:
                error='Password es requerido'
            elif c.fetchone() is not None:
                error = 'Usuario {} se encuentra registrado'.format(username)
            
            if error is None:
                c.execute(
                    'insert into user (username, password) values (%s, %s)',
                    (username, generate_password_hash(password))
                ) 
                db.commit()
                flash('ok')
                return redirect(url_for('auth.login'))
            flash(error)
        else:
            error='Contraseñas no coinciden'
            flash(error)
    # sql = 'select id from user'
    # c.execute(sql)   
    
    return render_template('auth/register.html')



@bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error= None
        c.execute(
            'select * from user where username = %s', (username,)
        )
        user=c.fetchone()
        
        if user is None:
            error = 'Ususario y/o contraseña inválida'
        elif not check_password_hash(user['password'], password):
            error = 'Ususario y/o contraseña inválida' 
        if error is None:
            session.clear()        
            session['user_id']=user['id']
            return redirect(url_for('crud.agrega_producto'))
        flash(error)
    return render_template('auth/login.html')



@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id == None:
        g.user = None
    else:
        db, c = get_db()
        c.execute(
            'select id, username from user where id = %s',(user_id,)
        )
        g.user = c.fetchone()

          
        
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        # preguntamos su usuario 
        # esta en nuestra variable 
        # global g
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


