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


@app.route('/add', methods=['POST'])
def Agregar():
    Dato = request.json['Datos']
    errors = {'Nombre': [], 'Season': [], 'Date': [], 'Number': []}
    existing_name = db.python.find_one({'Nombre': Dato['Nombre']})
    # giving the date format
    # date_format = '%Y-%m-%d'

    


    if existing_name:
        errors['Nombre'].append('Nombre ya se encuentra en uso')

    if not Dato.get('Nombre'):
        errors['Nombre'].append('Este campo es requerido')
    
    if not Dato.get('Season'):
        errors['Season'].append('Este campo es requerido')

    if not Dato.get('Date'):
       errors['Date'].append('Este campo es requerido')

    if not Dato.get('Number'):
        errors['Number'].append('Este campo es requerido')
    
    if len(Dato.get('Nombre')) > 15:
        errors['Nombre'].append('El campo Nombre no puede tener más de 15 caracteres')
    
    if not Dato['Number'].isdigit():
        errors['Number'].append('Este Campo solo debe contener Numeros')

        # try:
        #     # formatting the date using strptime() function
        #     datetime.datetime.strptime(Dato['Date'], date_format)
        # # If the date validation goes wrong
        # except ValueError:
        # # printing the appropriate text if ValueError occurs
        #     errors['Date'].append('Formato de fecha incorrecto, debe ser AAAA-MM-DD')

    if Dato['Season'].lower() not in ["primavera", "verano", "otoño", "invierno"]:
        errors['Season'].append('Ingrese solo las Estaciones de la epoca')


    if errors:
        return jsonify({'errors': errors}), 400
    else:
        _id = db.python.insert_one({
            'Nombre': Dato['Nombre'], 
            'Season': Dato['Season'], 
            'Date': Dato['Date'], 
            'Number': Dato['Number'],  
        })
        return jsonify({'id': str(_id.inserted_id), 'Nombre': Dato['Nombre']}),200





app.run(debug=True)