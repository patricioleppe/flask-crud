instructions = [
    # si por alguna razon 
    # tenemos que eliminar 
    # una tabla de la base, 
    # y no nos deje por que 
    # hay ref a llaves foraneas 
    # hacer esto:
    'SET FOREIGN_KEY_CHECKS=0;',
    
    'DROP TABLE IF EXISTS user;',
    'DROP TABLE IF EXISTS productos;',
    
    #luego de hacer esto puedo 
    # volver a darle seguridad 
    # para que no elimine tablas 
    # con referencias de llaves 
    # foraneas 
    'SET FOREIGN_KEY_CHECKS=1;',
    # triple comillas dobles:
    # me permite generar strings 
    # de multiples lineas .
    """
    CREATE TABLE user (
        id int PRIMARY KEY AUTO_INCREMENT, 
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        correo VARCHAR(255),
        telefono VARCHAR(12),
        estado CHAR(1),
        tipo char(1)
        
    )
    """,

    """ 
    CREATE TABLE productos(
        id int PRIMARY KEY AUTO_INCREMENT,
        nombre varchar(50),
        codigo varchar(50),
        descripcion varchar(100),
        marca varchar(50),
        tipo varchar(10)
    )"""
    , 
    """CREATE TABLE productos_tipo(
        id int PRIMARY KEY AUTO_INCREMENT,
        codigo varchar(50),
        descripcion varchar(100)
        
    )"""
    
] 