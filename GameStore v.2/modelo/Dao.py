from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Float,BLOB
from sqlalchemy.orm import relationship

from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
import datetime

db=SQLAlchemy()

class Categoria(db.Model):
    __tablename__='categorias'
    id_categoria=Column(Integer,primary_key=True)
    nombre=Column(String)
    imagen=Column(BLOB)
    estatus=Column(String)

    def consultarImagen(self,id):
        return self.consultaIndividual(id).imagen

    def consultaIndividual(self,id):
        return self.query.get(id)

    def consultaGeneral(self):
        return self.query.all()

    def editar(self):
        db.session.merge(self)
        db.session.commit()    

    def agregar(self):
        db.session.add(self)
        db.session.commit()  

    def eliminarCate(self,id):
        c=self.consultaIndividual(id)
        db.session.delete(c)
        db.session.commit()        

    def eliminacionLogica(self,id):
        c=self.consultaIndividual(id)
        c.estatus='Inactivo'
        c.editar()              

class Juego(db.Model):
    __tablename__='juegos'
    id_categoria=Column(Integer, ForeignKey('categorias.id_categoria'))
    nombre=Column(String)
    descripcion=Column(String)
    imagen=Column(BLOB)
    estatus=Column(String) 
    id_juego=Column(Integer, primary_key=True)
    precio=Column(Float)
    existencia=Column(Integer)
    categoria=relationship('Categoria',backref='juegos', lazy='select')

    def consultarImagen(self,id):
        return self.consultaIndividual(id).imagen

    def consultaIndividual(self,id):
        return self.query.get(id)    

    def consultaGeneral(self):
        return self.query.all()

    def editar(self):
        db.session.merge(self)
        db.session.commit()        

    def agregar(self):
        db.session.add(self)
        db.session.commit()         

    def eliminar(self,id):
        j=self.consultaIndividual(id)
        db.session.delete(j)
        db.session.commit()        

    def eliminacionLogica(self,id):
        j=self.consultaIndividual(id)
        j.estatus='Inactivo'
        j.editar() 

# Usuarios
class Usuario(UserMixin,db.Model):
    __tablename__='usuarios'
    id_usuario=Column(Integer,primary_key=True)
    nombreCompleto=Column(String,nullable=False)
    direccion=Column(String,nullable=False)
    telefono=Column(String,nullable=False)
    email=Column(String,unique=True)
    password_hash=Column(String(128),nullable=False)
    tipo=Column(String,nullable=False)
    estatus=Column(String,nullable=False)
    genero=Column(String,nullable=False)

    @property #Implementa el metodo Get (para acceder a un valor)
    def password(self):
        raise AttributeError('El password no tiene acceso de lectura')

    @password.setter #Definir el metodo set para el atributo password_hash
    def password(self,password):#Se informa el password en formato plano para hacer el cifrado
        print('password '+password)
        self.password_hash=generate_password_hash(password)
        print(' hash '+self.password_hash)


    def validarPassword(self,password):
        print('password '+password)
        print(' hash '+self.password_hash)

        return check_password_hash(self.password_hash,password)
    #Definición de los métodos para el perfilamiento
    def is_authenticated(self):
        return True

    def is_active(self):
        if self.estatus=='Activo':
            return True
        else:
            return False

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id_usuario

    def is_admin(self):
        if self.tipo=='Administrador':
            return True
        else:
            return False
    
    def is_vendedor(self):
        if self.tipo=='Vendedor':
            return True
        else:
            return False
    
    def is_cliente(self):
        if self.tipo=='Cliente':
            return True
        else:
            return False
    #Definir el método para la autenticacion
    def validar(self,email,password):
        usuario=Usuario.query.filter(Usuario.email==email).first()
        #print(usuario.email)
        if usuario!=None and usuario.validarPassword(password) and usuario.is_active():
            return usuario
        else:
            return None
    #Método para agregar una cuenta de usuario
    def agregar(self):
        db.session.add(self)
        db.session.commit()

# Carrito
class Carrito(db.Model):
    __tablename__='carrito'
    id_carrito=Column(Integer,primary_key=True)
    id_usuario=Column(Integer, ForeignKey('usuarios.id_usuario'))
    id_juego=Column(Integer, ForeignKey('juegos.id_juego'))
    cantidad=Column(Integer)
    juego=relationship('Juego',backref='carrito', lazy='select')
    usuario=relationship('Usuario',backref='carrito', lazy='select')
    
    def agregar(self):
        db.session.add(self)
        db.session.commit()
        
    def consultaGeneral(self,id_usuario):
        return self.query.filter(Carrito.id_usuario==id_usuario).all()