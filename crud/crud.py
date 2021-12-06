from logging import RootLogger, error
from flask import (Blueprint, flash, g, redirect, render_template,request, url_for, make_response)
from flask.json import jsonify
from werkzeug.exceptions import abort
from crud.auth import login_required
from crud.db import get_db
import json


bp = Blueprint('crud', __name__)

# despues de logearnos
@bp.route('/')
@login_required
def modulos():
    db, c = get_db()
    sql="select id , numero, nombre, descripcion FROM modulos"
    c.execute(sql)    
    mo = c.fetchall()
    return render_template('crud/index.html', mod=mo)


@bp.route('/agrega_producto', methods=['GET','POST'])
@login_required
def agrega_producto():
    db, c = get_db()
    if request.method == 'POST':
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        marca = request.form['marca']
        tipo = request.form['tipo']
        
        sql="SELECT count(*) as cont FROM productos where codigo=%s"
        c.execute(sql,(codigo,))
        dato = c.fetchone()
        dat=dato['cont']
        
        error = None
       
        if dat > 0:
            error="Codigo ya existe, no se puede grabar."
           
            #return redirect(url_for('todo.agrega_producto',hol=hol))
            
        elif not codigo:
            error="Ingrese un codigo, es requerido"
        elif not nombre:
            error="Ingrese un codigo es requerida"
        elif not descripcion:
            error="Ingrese un codigo es requerida"
        elif not marca:
            error="Ingrese un codigo es requerida"
        elif not tipo:
            error="Ingrese un codigo es requerida"
        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            sql='INSERT into productos (codigo, nombre, descripcion, marca, tipo) values (UPPER(%s), %s, %s, %s, %s)'
            c.execute(sql,(codigo,nombre,descripcion,marca,tipo))
            db.commit()
            return redirect(url_for('crud.agrega_producto'))
      
    sql="SELECT id, codigo, descripcion FROM productos_tipo"
    c.execute(sql)
    ti = c.fetchall()
    
    sql="SELECT id, nombre, codigo, descripcion, marca, tipo FROM productos order by id desc"
    c.execute(sql)
    pro = c.fetchall()
    return render_template('crud/agrega_producto.html',tip=ti, prod=pro)
    
@bp.route('/genera_codigo', methods=['POST','GET'])
@login_required
def genera_codigo():
    
    if request.method == 'POST':
        tipo = request.get_json()
        dato=tipo['tipo']
        
        db, c = get_db()
        sql='SELECT MAX(SUBSTRING(codigo , 5 , 6 )) as cod  from productos WHERE tipo=%s order by id desc'
        c.execute(sql,(dato,))
        data = c.fetchone()
        if data['cod'] == None:
            data = dato+'000001'
        else:
            data=int(data['cod'])
            data=data+1
            # print(data)
            data=str(data).zfill(6);
            # print(data)
            data = dato+data
            # data['cod']=d 
            # print(dato+data)
           
        #resp = make_response(jsonify({"data":data}))
        resp = make_response(jsonify({"data":data}))
        return (resp)

@bp.route('/edita_producto/<id>')
@login_required
def edita_producto(id):
    db, c = get_db()
    sql='SELECT id, nombre, codigo, descripcion, marca, tipo from productos where id=%s'
    print(sql)
    c.execute(sql,(id,))
    pro = c.fetchone()
    
    sql="SELECT codigo, descripcion FROM productos_tipo"
    c.execute(sql)
    ti = c.fetchall()
    
    return render_template('crud/edita_producto.html', prod=pro, tip=ti)

    
@bp.route('/actualiza_producto/<id>',methods=['GET','POST'])
@login_required
def actualiza_producto(id):
    if request.method == 'POST':
        
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        marca = request.form['marca']
        
        
        error=None
       
        if not nombre:
            error="Ingrese un Nombre"
        elif not descripcion:
            error="Ingrese una Descripcion"
        elif not marca:
            error="Ingrese una Marca"
        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            sql='UPDATE productos set nombre=%s, descripcion=%s, marca=%s  WHERE id=%s'
            print (sql)
            c.execute(sql,(nombre, descripcion, marca, id))
            db.commit()
        return redirect(url_for('crud.agrega_producto'))
    return render_template('crud/agrega_producto.html')
    
@bp.route('/borrar_producto/<id>', methods=['POST','GET'])
@login_required
def borrar_producto(id):
    db, c = get_db()
    sql='delete from productos where id = %s'
    c.execute(sql,(id,))
    db.commit()
    return redirect(url_for('crud.agrega_producto'))
