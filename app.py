from flask import Flask ,jsonify,request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app=Flask(__name__)
CORS(app)

#ingreso base de datos declarando usuario y clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://sql10508509:3EEiB3tXqc@sql10.freemysqlhosting.net/sql10508509'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
ma=Marshmallow(app)
'''
Server: sql10.freemysqlhosting.net
Name: sql10508509
Username: sql10508509
Password: 3EEiB3tXqc
Port number: 3306
'''

#clase Insumos hereda db.model
class Insumos(db.Model):
    idinsumo=db.Column(db.Integer, primary_key=True)
    articulo=db.Column(db.String(100))
    preciounitario=db.Column(db.Float)
    cantidad=db.Column(db.Integer)
    def __init__(self,articulo,preciounitario,cantidad): 
        self.articulo=articulo   # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.preciounitario=preciounitario
        self.cantidad=cantidad
db.create_all()

class InsumosSchema(ma.Schema):
    class Meta:
        fields=('idinsumo','articulo','preciounitario','cantidad')
insumo_schema=InsumosSchema()            # para crear un producto
insumos_schema=InsumosSchema(many=True)  # multiples registros

@app.route('/')
def index():
    return "<h1>Corriendo servidor Flask</h1>"

@app.route('/insumos',methods=['GET'])
def get_Insumos():
    all_insumos=Insumos.query.all()     # query.all() lo hereda de db.Model
    result=insumos_schema.dump(all_insumos)  # .dump() lo hereda de ma.schema
    return jsonify(result)
@app.route('/insumos/<id>',methods=['GET'])
def get_insumos(id):
    insumo=Insumos(articulo, preciounitario, cantidad).query.get(id)
    return insumo_schema.jsonify(insumo)

#hasta aca insumos

@app.route('/insumos/<id>',methods=['DELETE'])
def delete_insumo(id):
    insumos=Insumos.query.get(id)
    db.session.delete(insumos)
    db.session.commit()
    return insumo_schema.jsonify(insumos)

@app.route('/insumos', methods=['POST']) # crea ruta o endpoint
def create_insumo():
    print(request.json)  # request.json contiene el json que envio el cliente
    articulo=request.json['articulo']
    preciounitario=request.json['preciounitario']
    cantidad=request.json['cantidad']
    new_insumo=Insumos(articulo, preciounitario, cantidad)
    db.session.add(new_insumo)
    db.session.commit()
    return insumo_schema.jsonify(new_insumo)

@app.route('/insumos/<id>' ,methods=['PUT'])
def update_insumo(id):
    insumo=Insumos.query.get(id)
   
    articulo=request.json['articulo']
    preciounitario=request.json['preciounitario']
    cantidad=request.json['cantidad']
 
    insumo.articulo=articulo
    insumo.preciounitario=preciounitario
    insumo.cantidad=cantidad
    db.session.commit()
    return insumo_schema.jsonify(insumo)



if __name__=='__main__':  
    app.run(debug=True)  

#, port=5000
