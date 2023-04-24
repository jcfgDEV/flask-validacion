from flask import Flask,request,jsonify
from pymongo import MongoClient
from flask_cors import CORS
import re
import datetime
from dateutil.parser import parse
app = Flask(__name__)
CORS(app)


client = MongoClient('mongodb+srv://ObscureBM:WfhEnDVw90w8FVSU@cluster0.imwio.mongodb.net/?retryWrites=true&w=majority')
db = client.test


@app.route('/', methods=['GET'])
def Home():
    response = {
        "Name": "John Developer",
        "Status": "200",
    }
    return response


# @app.route('/add', methods=['POST'])
# def Agregar():
#     Dato = request.json['Datos']
#     errors = {'Nombre': [], 'Season': [], 'Date': [], 'Number': []}
#     existing_name = db.python.find_one({'Nombre': Dato['Nombre']})
#     # FORMATO DE LA FECHA
#     date_format = '%Y-%m-%d'

#     if existing_name:
#         errors['Nombre'].append('Ya se encuentra ese nombre')
    
#     if not Dato['Nombre']:
#         errors['Nombre'].append('Este campo es requerido')

#     if not Dato['Season']:
#         errors['Season'].append('Este campo es requerido')

#     if not Dato['Date']:
#        errors['Date'].append('Este campo es requerido')

#     if not Dato['Number']:
#         errors['Number'].append('Este campo es requerido')

#     if len(Dato['Nombre']) > 15:
#         errors['Nombre'].append('El campo Nombre no puede tener más de 15 caracteres')

#     if not Dato['Number'].isdigit():
#         errors['Number'].append('Este Campo solo debe contener Numeros')


#         try:
#             datetime.datetime.strptime(Dato['Date'], date_format)
#             # si la fecha da errado en el formato lanzara una exepcion
#         except ValueError:
#             # printing the appropriate text if ValueError occurs
#             errors['Date'].append('Formato de fecha incorrecto, debe ser AAAA-MM-DD')
#         finally:
#             return

#     if Dato['Season'].lower() not in ["primavera", "verano", "otoño", "invierno"]:
#         errors['Season'].append('Ingrese solo las Estaciones de la epoca')
#     return jsonify({'errors': errors}), 400


#     inserted_record = db.python.insert_one({
#         'Nombre': Dato['Nombre'], 
#         'Season': Dato['Season'], 
#         'Date': Dato['Date'], 
#         'Number': Dato['Number'],  
#     })

#     return jsonify({'id': str(inserted_record.inserted_id)}),200


@app.route('/add', methods=['POST'])
def Agregar():
    Dato = request.json['Datos']
    errors = {'Nombre': [], 'Season': [], 'Date': [], 'Number': []}
    existing_name = db.python.find_one({'Nombre': Dato['Nombre']})
    # FORMATO DE LA FECHA
    date_format = '%Y-%m-%d'

    if existing_name:
        errors['Nombre'].append('Ya se encuentra ese nombre')
    
    if not Dato.get('Nombre'):
        errors['Nombre'].append('Este campo es requerido')

    if not Dato.get('Season'):
        errors['Season'].append('Este campo es requerido')

    if not Dato.get('Date'):
       errors['Date'].append('Este campo es requerido')
    else:
        try:
            datetime.datetime.strptime(Dato['Date'], date_format)
        except ValueError:
            errors['Date'].append('Formato de fecha incorrecto, debe ser AAAA-MM-DD')

    if not Dato.get('Number'):
        errors['Number'].append('Este campo es requerido')
    elif not Dato['Number'].isdigit():
        errors['Number'].append('Este campo solo debe contener números')

    if len(Dato.get('Nombre', '')) > 15:
        errors['Nombre'].append('El campo Nombre no puede tener más de 15 caracteres')

    season_options = ["primavera", "verano", "otoño", "invierno"]
    if not Dato.get('Season') or Dato['Season'].lower() not in season_options:
        errors['Season'].append('Debe Ingresar: ' + ', '.join(season_options))

    if any(errors.values()):
        return jsonify({'errors': errors}), 400

    _id = db.python.insert_one({
        'Nombre': Dato['Nombre'], 
        'Season': Dato['Season'].lower(),  # Convertir a minúsculas
        'Date': Dato['Date'], 
        'Number': Dato['Number'],  
    })

    return jsonify({'id': str(_id.inserted_id)}), 200



app.run(debug=True)