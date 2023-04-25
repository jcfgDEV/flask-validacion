from flask import Flask,request,jsonify
from pymongo import MongoClient
from flask_cors import CORS
from dotenv import load_dotenv
import datetime
import os
# Carga las variables de entorno desde el archivo .env
load_dotenv()
app = Flask(__name__)
CORS(app)


# mongo_uri = os.environ.get('MONGO_URI')
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
    Data = request.json['Datos']
    errors = {'Nombre': [], 'Season': [], 'Date': [], 'Number': []}
    existing_name = db.python.find_one({'Nombre': Data['Nombre']})
    # FORMATO DE LA FECHA
    date_format = '%Y-%m-%d'

    if existing_name:
        errors['Nombre'].append('Ya se encuentra ese nombre')
    
    if not Data['Nombre']:
        errors['Nombre'].append('Este campo es requerido')

    if not Data['Season']:
        errors['Season'].append('Este campo es requerido')

    if not Data['Date']:
       errors['Date'].append('Este campo es requerido')
    else:
        try:
            datetime.datetime.strptime(Data['Date'], date_format)
        except ValueError:
            errors['Date'].append('Formato de fecha incorrecto, debe ser AAAA-MM-DD')

    if not Data['Number']:
        errors['Number'].append('Este campo es requerido')
    elif not Data['Number'].isdigit():
        errors['Number'].append('Este campo solo debe contener números')

    if len(Data['Nombre']) > 15:
        errors['Nombre'].append('El campo Nombre no puede tener más de 15 caracteres')

    season_options = ["primavera", "verano", "otoño", "invierno"]
    if not Data['Season'] or Data['Season'].lower() not in season_options:
        errors['Season'].append('Debe Ingresar: ' + ', '.join(season_options))

    if any(errors.values()):
        return jsonify({'errors': errors}),422

    _id = db.python.insert_one({
        'Nombre': Data['Nombre'], 
        'Season': Data['Season'].lower(),  # Convertir a minúsculas
        'Date': Data['Date'], 
        'Number': Data['Number'],  
    })

    return jsonify({'id': str(_id.inserted_id)}),200


if __name__ == '__main__':
    app.run(debug=True)