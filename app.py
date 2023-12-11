"""La línea de comando:
pip install Flask SQLAlchemy mysql-connector-python 

se utiliza para instalar
tres paquetes en tu entorno de Python. 
Aquí está una breve descripción de cada uno de ellos:

Flask: Flask es un framework ligero de desarrollo
web para Python. Facilita la creación de aplicaciones
web de manera rápida y sencilla. Con Flask, puedes
definir rutas, gestionar solicitudes HTTP, y construir
aplicaciones web de manera eficiente.

SQLAlchemy: SQLAlchemy es una biblioteca de
SQL en Python que proporciona un conjunto
de herramientas de alto nivel para interactuar
con bases de datos relacionales. Facilita la
creación, el acceso y la manipulación de bases
de datos utilizando objetos Python en lugar de escribir directamente SQL.

mysql-connector-python: Este paquete es un conector oficial
de MySQL para Python. Permite a tu aplicación Python conectarse y 
comunicarse con una base de datos MySQL. En el contexto de Flask
y SQLAlchemy, se utiliza para establecer la conexión entre tu 
aplicación y la base de datos MySQL ."""

# 3. Importar las herramientas
# Acceder a las herramientas para crear la app web
from flask import Flask, request, jsonify

# Para manipular la DB
from flask_sqlalchemy import SQLAlchemy 

# Módulo cors es para que me permita acceder desde el frontend al backend
from flask_cors import CORS

# 4. Crear la app
app = Flask(__name__)

# Habilitar a la app para recibir peticiones
CORS(app)


# 5. Configurar a la app la DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://usuario:contraseña@localhost:3306/nombre_de_la_base_de_datos'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/amapoladb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 6. Crear un objeto db, para informar a la app que se trabajará con sqlalchemy
db = SQLAlchemy(app)

# 7. Definir la tabla 
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    price = db.Column(db.Float(50))
    description =db.Column(db.String(300))
    category = db.Column(db.String(50))
    image = db.Column(db.String(200))


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)       
    nombre = db.Column(db.String(100))
    sexo = db.Column(db.String(100))
    usuario = db.Column(db.String(100))
    contraseña = db.Column(db.String(200))





# 8. Crear la tabla al ejecutarse la app
with app.app_context():
    db.create_all()

# Crear ruta de acceso
# / es la ruta de inicio
@app.route("/")
def index():
    return f'App Web para registrar nombres de productos y usuarios'

# Recibir los datos que vienen del formulario 
# para insertarlos en la DB

#--------------------------NUEVO Producto------------------------
@app.route("/registro", methods=['POST'])
def registro():
    #      <input type="text" name="nombre" id="nombre">
    # {
    #   "nombre": "Luis"
    # }
    titulo_recibido = request.json["title"]
    precio_recibido=request.json["price"]
    descripcion_recidido=request.json["description"]
    categoria_recibido=request.json["category"]
    imagen_recibido=request.json["image"]

    # ¿Cómo insertar el registro en la tabla?
    nuevo_registro = Producto(
        title=titulo_recibido,
        price=precio_recibido,
        description=descripcion_recidido,
        category=categoria_recibido,
        image=imagen_recibido
        )
    db.session.add(nuevo_registro)
    db.session.commit()

    return "Solicitud via post recibida"
#--------------------------------------------------------------------------------------------------

#----------------------Obtener Todos los Productos-----------------------------------------------
# Retornar todos los registros de la tabla productos, en un Json
@app.route("/productos",  methods=['GET'])
def productos():
    # Consultar la tabla producto y traer todos los registros
    # all_registros -> lista de objetos
    all_registros = Producto.query.all()

    data_serializada = [] # Lista de diccionarios
    for registro in all_registros:
        data_serializada.append({
            "id":registro.id,
            "title":registro.title,
            "price":registro.price,
            "description":registro.description,
            "category":registro.category,
            "image":registro.image
            })

    # transformar a json
    return jsonify(data_serializada)

#----------------------Obtener un Registro-----------------------------------------------
# Retornar  un registro de la tablaa productos, en un Json
@app.route("/producto/<id>",  methods=['GET'])
def producto(id):
    # Consultar la tabla producto y trae un  registro
    # registro -> un producto
    registro = Producto.query.get(id)

    

    data_serializada = {
        "id":registro.id,
        "title":registro.title,
        "price":registro.price,
        "description":registro.description,
        "category":registro.category,
        "image":registro.image
        } 
   

    # transformar a json
    return jsonify(data_serializada)

#-------------------------------------------------------------------------------------------------------------


#-------------------------Obtener Todos los Producto de una Categoria Especifica--------------------------------------------
# Retornar  un registro de la tablaa productos, en un Json
@app.route("/productos/category/<category>",  methods=['GET'])
def categoria(category):
    # Consultar la tabla producto y trae un  registro
    # registro -> un producto
    registros = Producto.query.filter_by(category=category)

    data_serializada = [] # Lista de diccionarios
    for registro in registros:
        data_serializada.append({
            "id":registro.id,
            "title":registro.title,
            "price":registro.price,
            "description":registro.description,
            "category":registro.category,
            "image":registro.image
            })

    

    

    # transformar a json
    return jsonify(data_serializada)

#-------------------------------------------------------------------------------------------------------------

#-------------------------Obtener Todos los Producto Con limite 5--------------------------------------------
# Retornar  un registro de la tablaa productos, en un Json
@app.route("/productos/limite=5",  methods=['GET'])
def limite():
    # Consultar la tabla producto y trae un  registro
    # registro -> un producto
    registros = Producto.query.limit(5).all()

    data_serializada = [] # Lista de diccionarios
    for registro in registros:
        data_serializada.append({
            "id":registro.id,
            "title":registro.title,
            "price":registro.price,
            "description":registro.description,
            "category":registro.category,
            "image":registro.image
            })

    

    

    # transformar a json
    return jsonify(data_serializada)

#-------------------------------------------------------------------------------------------------------------

#-------------------------Obtener Todos los Producto  ordenado por categoria decendiente--------------------------------------------
# Retornar  un registro de la tablaa productos, en un Json
@app.route("/productos/decendiente",  methods=['GET'])
def categoriaDecendiente():
    # Consultar la tabla producto y trae un  registro
    # registro -> un producto
    registros = Producto.query.order_by(Producto.category.desc()).all()

    data_serializada = [] # Lista de diccionarios
    for registro in registros:
        data_serializada.append({
            "id":registro.id,
            "title":registro.title,
            "price":registro.price,
            "description":registro.description,
            "category":registro.category,
            "image":registro.image
            })

    

    

    # transformar a json
    return jsonify(data_serializada)

#-------------------------------------------------------------------------------------------------------------
# --------------------------------Modificar un registro-------------------------------------------------
@app.route('/update/<id>', methods=['PUT'])
def update(id):
    # Buscar el registro por el id
    update_producto = Producto.query.get(id)

    # Recibir los nuevos datos a guardar
    titulo = request.json["title"]
    precio = request.json["price"]
    descripcion = request.json["description"]
    categoria = request.json["category"]
    imagen = request.json["image"]

    # Sobreescribir la info
    update_producto.title = titulo
    update_producto.price = precio
    update_producto.description = descripcion    
    update_producto.category = categoria
    update_producto.image = imagen
    db.session.commit()

    data_serializada = [{"id": update_producto.id,"title": update_producto.title,"price":update_producto.price,"category":update_producto.category,"image":update_producto.image}]
    return jsonify(data_serializada)

    #--------------------------------------------------------------------------------------------------------------------
#---------------------------- Eliminar una persona de la tabla persona por id
@app.route('/borrar/<id>', methods=['DELETE'])
def borrar(id):
    # Buscar el registro por el id
    delete_producto = Producto.query.get(id)

    db.session.delete(delete_producto)
    db.session.commit()

    data_serializada = [{"id": delete_producto.id, "title": delete_producto.title,"price":delete_producto.price,"description":delete_producto.description,"category":delete_producto.category,"image":delete_producto.image}]
    return jsonify(data_serializada)

#------------------------------------------------------------------------------------------------

#####################SECCION USUARIO##########################################################################################


#--------------------------logueo--------------------
@app.route("/login", methods=['POST'])
def login():

    user_recibida=request.json['usuario']
    pass_recibida=request.json['pass']   


    # print(user_recibida,pass_recibida)
    registro = Usuario.query.filter_by(usuario=user_recibida ,contraseña=pass_recibida ).first()

    data_serializada = {

       "id":registro.id,
        "nombre":registro.nombre,            
        "usuario":registro.usuario,
        "contraseña":registro.contraseña,
        "sexo":registro.sexo
    }   
 

    return jsonify(data_serializada)

#-------------------------------------------------------------------------------------------------
#----------------------Obtener Todos los Usuarios-----------------------------------------------
# Retornar todos los registros de la tabla usuarios, en un Json
@app.route("/usuarios",  methods=['GET'])
def usuarios():
    # Consultar la tabla usuarios y traer todos los registros
    # all_registros -> lista de objetos
    all_registros = Usuario .query.all()

    data_serializada = [] # Lista de diccionarios
    for registro in all_registros:
        data_serializada.append({
            "id":registro.id,
            "nombre":registro.nombre,            
            "usuario":registro.usuario,
            "contraseña":registro.contraseña,
            "sexo":registro.sexo
            })

    # transformar a json
    return jsonify(data_serializada)
#--------------------------------------------------------------------------------------------------
#--------------------------NUEVO USUARIO------------------------
@app.route("/registrousuario", methods=['POST'])
def registrousuario():
    #      <input type="text" name="nombre" id="nombre">
    # {
    #   "nombre": "Luis"
    # }
    nombre_recibido = request.json["nombre"]
    usuario_recibido=request.json["usuario"]
    contraseña_recidido=request.json["contraseña"]
    sexo_recibido=request.json["sexo"]
    

    # ¿Cómo insertar el registro en la tabla?
    nuevo_registro = Usuario(
        nombre=nombre_recibido,
        usuario=usuario_recibido,
        contraseña=contraseña_recidido,
        sexo=sexo_recibido,
        
        )
    db.session.add(nuevo_registro)
    db.session.commit()

    return "Solicitud via post recibida"
#--------------------------------------------------------------------------------------------------
# --------------------------------Modificar un registro-------------------------------------------------
@app.route('/updateusuario/<id>', methods=['PUT'])
def updateusuario(id):
    # Buscar el registro por el id
    update_usuario = Usuario.query.get(id)

    # Recibir los nuevos datos a guardar
    nombre = request.json["nombre"]
    usuario = request.json["usuario"]
    contraseña = request.json["contraseña"]
    sexo = request.json["sexo"]
    

    # Sobreescribir la info
    update_usuario.nombre = nombre
    update_usuario.usuario = usuario
    update_usuario.contraseña = contraseña    
    update_usuario.sexo = sexo
    
    db.session.commit()

    data_serializada = [{"id": update_usuario.id,"nombre": update_usuario.nombre,"usuario":update_usuario.usuario,"contraseña":update_usuario.contraseña,"sexo":update_usuario.sexo}]
    return jsonify(data_serializada)

    #--------------------------------------------------------------------------------------------------------------------
#---------------------------- Eliminar un usuario de la tabla persona por id
@app.route('/borrarusuario/<id>', methods=['DELETE'])
def borrarusuario(id):
    # Buscar el registro por el id
    delete_usuario = Usuario.query.get(id)

    db.session.delete(delete_usuario)
    db.session.commit()

    data_serializada = [{"id": delete_usuario.id,"nombre": delete_usuario.nombre,"usuario":delete_usuario.usuario,"contraseña":delete_usuario.contraseña,"sexo":delete_usuario.sexo}]
    return jsonify(data_serializada)

#------------------------------------------------------------------------------------------------







if __name__ == "__main__":
    app.run(debug=True)

