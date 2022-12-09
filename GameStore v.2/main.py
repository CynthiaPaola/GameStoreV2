from flask import Flask, redirect, render_template, request, url_for
from modelo.Dao import Categoria, Juego, db, Usuario, Carrito
# gestion de cuentas de usuario
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import  session,redirect, url_for
from datetime import timedelta
import json
# Boostrap
from flask_bootstrap import Bootstrap

app = Flask(__name__)


#base de datos
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost/gamestore' #cadena de conexion
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

#boostrap
Bootstrap(app)

#gestion de usuarios
app.secret_key='Cl4v3'
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='index'
login_manager.login_message='¡ Tu sesión expiró !'
login_manager.login_message_category="info"

@login_manager.user_loader
def cargar_usuario(id):
    return Usuario.query.get(int(id))

# Urls definidas para el control de usuario
@app.before_request
def before_request():
    session.permanent=True
    app.permanent_session_lifetime=timedelta(minutes=10)

@app.route('/cerrarSesion')
@login_required
def cerrarSesion():
    logout_user()
    return redirect(url_for('index'))# nombre de la vista o 
    #funcion que carga el formulario para iniciar sesion
    
#rutas
@app.route('/')
def index():
    return render_template('principal.html')

@app.route('/registrarUsuario', methods=['GET','post'])
def regUser():
    if request.method=='POST':
        userN=Usuario()
        userN.nombreCompleto=request.form['nombreUsuario']
        userN.direccion=request.form['direccion']
        userN.telefono=request.form['telefono']
        userN.email=request.form['correo']
        userN.password=request.form['contrasena']
        userN.genero=request.form['genero']
        userN.tipo='Cliente'
        userN.estatus='Activo'
        userN.agregar()
        return redirect(url_for('index'))
    return render_template('registrarUsuarios.html')    

@app.route('/validar', methods=['post'])
def validar():
    correo=request.form['correo']
    contrasena=request.form['contrasena']
    u=Usuario()
    uBD=u.validar(correo,contrasena)
    if uBD !=None:
        login_user(uBD)
        return redirect(url_for('regresar', persona=uBD.nombreCompleto))
    return render_template ('login.html',aviso='datos incorrectos')

# juegos
@app.route('/juegos', methods=['GET'])
@login_required
def juegos():
    game=Juego()
    games=game.consultaGeneral()
    return render_template('juegos/juegos.html', games=games)

@app.route('/juegos/consultarImagen/<int:id>')
def consultarImagenJuego(id):
    game=Juego()
    return game.consultarImagen(id)    

@app.route('/registrarJuego', methods=['GET', 'POST'])
@login_required
def registrarJuego():
    if current_user.is_admin() or current_user.is_vendedor(): 
        if request.method == 'POST':
            gameA=Juego()
            gameA.nombre=request.form['nombreJuego']
            gameA.descripcion=request.form['descJuego']
            gameA.precio=request.form['precioJuego']
            gameA.existencia=request.form['existJuego']
            gameA.id_categoria=request.form['categoria']
            gameA.imagen=request.files['imagenJuego'].stream.read()
            gameA.estatus='Activo'
            gameA.agregar()
            return redirect(url_for('juegos'))
        cate=Categoria()
        cates=cate.consultaGeneral()    
        return render_template('juegos/registrarJuego.html', cates=cates)
    return redirect(url_for('juegos'))

@app.route('/actualizarJuego/<int:numJuego>', methods=['GET', 'POST'])
@login_required
def actualizarJuego(numJuego):
    if current_user.is_admin() or current_user.is_vendedor():
        if request.method == 'POST':
            gameA=Juego()
            gameA.id_juego=numJuego
            gameA.nombre=request.form['nombreJuego']
            gameA.descripcion=request.form['descJuego']
            gameA.precio=request.form['precioJuego']
            gameA.existencia=request.form['existJuego']
            gameA.id_categoria=request.form['categoria']
            gameA.imagen=request.files['imagenJuego'].stream.read()
            gameA.estatus='Activo'
            gameA.editar()
            return redirect(url_for('juegos'))  
        cat=Categoria()
        cates=cat.consultaGeneral()
        j=Juego() 
        j=j.consultaIndividual(numJuego)    
        return render_template('/juegos/actualizarJuego.html', game=j, cates=cates)
    return redirect(url_for('juegos'))

@app.route('/eliminarJuegos/<int:numJuego>', methods=['GET', 'POST'])
@login_required
def eliminarJuego(numJuego):
    if current_user.is_admin() or current_user.is_vendedor():
        j=Juego()
        j.eliminar(numJuego)
        return redirect(url_for('juegos'))  
    return redirect(url_for('productos'))

@app.route('/videojuego/<int:numJuego>', methods=['get', 'POST'])
def verVideojuego(numJuego):
    # fin juegos

    precios = ['', '200', '67', '160', '300', '400', '600']
    return 'el videojuego que elegiste es: ' + juegos[numJuego]+' y su precio es ' + precios[numJuego]


# categorias
@app.route('/categorias', methods=['GET'])
@login_required
def categorias():
    cat=Categoria()
    cate=cat.consultaGeneral()
    return render_template('categorias/categorias.html', cate=cate)

@app.route('/categorias/consultarImagen/<int:id>')
def consultarImagenCat(id):
    cat=Categoria()
    return cat.consultarImagen(id)  

@app.route('/registrarCategoria', methods=['GET','POST'])
@login_required
def registrarCategoria():
    if current_user.is_admin():
        if request.method=='POST':
            nomCat=request.form['nombreCat']
            #codigo para guardar en la BD
            catN=Categoria()
            catN.nombre=nomCat
            catN.imagen=request.files['imagenCat'].stream.read()
            catN.estatus='Activa'
            catN.agregar()
            return redirect(url_for('categorias'))
            #return'categoria guardada'
        return render_template('categorias/registrarCategoria.html') 
    return redirect(url_for('categorias'))

@app.route('/actualizarCategoria/<int:numCategoria>', methods=['GET', 'POST'])
@login_required
def actualizarCategoria(numCategoria):
    if current_user.is_admin():
        if request.method == 'POST':
            catN=Categoria()
            catN.id_categoria=numCategoria
            nomCat=request.form['nombreCat']
            catN.nombre=nomCat
            catN.imagen=request.files['imagenCat'].stream.read()
            catN.estatus='Activa'
            catN.editar()
            return redirect(url_for('categorias'))  
        c=Categoria() 
        c=c.consultaIndividual(numCategoria)
        return render_template('categorias/actualizarCategoria.html', cat=c)
    return redirect(url_for('categorias'))

@app.route('/eliminarCategoria/<int:numCategoria>', methods=['GET', 'POST'])
@login_required
def eliminarCategoria(numCategoria):
    if current_user.is_admin():
        c=Categoria()
        c.eliminarCate(numCategoria)
    return redirect(url_for('categorias'))

#Carrito
@app.route('/carrito/agregar/<data>', methods=['GET', 'POST'])
@login_required
def agregarCarrito(data): 
    if current_user.is_authenticated and current_user.is_cliente():
        if request.method == 'POST':
            car=json.loads(data)
            carrito=Carrito()
            carrito.id_juego=car['id_juego']
            carrito.id_usuario=current_user.id_usuario
            carrito.cantidad=car['cantidad']
            carrito.agregar()
            msg={'estatus':'ok','mensaje':'Producto agregado a la cesta.'}
    else:
        msg = {"estatus": "error", "mensaje": "Debes iniciar sesion"}
    return json.dumps(msg)

@app.route('/carrito')
@login_required
def consultarCarrito():
    if current_user.is_authenticated:
        carrito=Carrito()
        return render_template('carrito/carrito.html',carrito=carrito.consultaGeneral(current_user.id_usuario))
    else:
        return redirect(url_for('index'))

# Login
@app.route('/loguearse', methods=['GET'])
def loguearse():
    return render_template('login.html')


@app.route('/regresar', methods=['GET'])
def regresar():
    return render_template('menu.html')


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
#  python -m venv venv  crear el entorno virtula 
# venv\scripts\activate.bat actva el entorno virtual
# pip instal flask para instalar flask solo una ves
# python -m main levantar el servidos 