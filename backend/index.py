from flask import Flask,request,jsonify
from pymongo import MongoClient
from flask_cors import CORS
import datetime
import os
from dotenv import load_dotenv
app = Flask(__name__)
CORS(app)
# Carga las variables de entorno desde el archivo .env
load_dotenv()

mongo_uri = os.environ.get('MONGO_URI')
client = MongoClient(mongo_uri)
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