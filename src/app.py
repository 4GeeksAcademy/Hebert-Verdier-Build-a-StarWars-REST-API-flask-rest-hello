"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from datetime import date
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Vehicle, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# ENDPOINTS
@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# USERS
# GET USERS / OBTENER USUARIOS
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    if len(users) == 0:
        return jsonify('no users found'), 404
    else: 
        data_serialized = list(map(lambda user: user.serialize(), users)) 
        return jsonify(data_serialized), 200

# GET ONE USER / OBTENER UN USUARIO
@app.route('/user/<int:id>', methods=['GET'])
def get_one_user(id):
    user = User.query.filter_by(id=id).first()
    if user == None:
        return jsonify('user not found'), 404
    else:
        user_serialized = user.serialize()
        return jsonify(user_serialized), 200

# POST USER / AÑADIR USUARIO
@app.route('/user', methods=['POST'])
def post_user():
    user = request.get_json()
    user_by_email = User.query.filter_by(email=user['email']).first()

    if not isinstance(user['name'], str) or len(user['name'].strip()) == 0:
         return({'error':'"name" must be a string'}), 400
    if not isinstance(user['last_name'], str) or len(user['last_name'].strip()) == 0:
         return({'error':'"last_name" must be a string'}), 400
    if not isinstance(user['email'], str) or len(user['email'].strip()) == 0:
         return({'error':'"email" must be a string'}), 400
    if user_by_email:
        if user_by_email.email == user['email']:
            return jsonify('This email is already used'), 403
    if not isinstance(user['password'], str) or len(user['password'].strip()) == 0:
         return({'error':'"password" must be a string'}), 400
    # if not isinstance(user['subscription_date'], date) or len(user['subscription_date'].strip()) == 0:
    #      return({'error':'"subscription_date" must be a date'}), 400

    user_created = User(name=user['name'], last_name=user['last_name'], email=user['email'], password=user['password'], subscription_date=date.today())
    db.session.add(user_created)
    db.session.commit()
    return jsonify(user_created.serialize()), 200

# DELETE ONE USER / ELIMINAR UN USUARIO
@app.route('/user/<int:id>', methods=['DELETE'])
def delete_one_user(id):
    user = User.query.filter_by(id=id).first()
    if user == None:
        return jsonify('user not found'), 404
    else:
        db.session.delete(user)
        db.session.commit()
        return jsonify('user deleted'), 200

# CHARACTERS
# GET CHARACTERS / OBTENER PERSONAJES
@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    if len(characters) == 0:
        return jsonify('no characters found'), 404
    else: 
        # data_serialized = [character.serialize() for character in characters]   ALTERNATIVA AL MAP
        data_serialized = list(map(lambda character: character.serialize(), characters)) 
        return jsonify(data_serialized), 200

# GET ONE CHARACTER / OBTENER UN PERSONAJE
@app.route('/character/<int:id>', methods=['GET'])
def get_one_character(id):
    character = Character.query.filter_by(id=id).first()
    if character == None:
        return jsonify('character not found'), 404
    else:
        character_serialized = character.serialize()
        return jsonify(character_serialized), 200

# POST CHARACTER / AÑADIR PERSONAJE
@app.route('/character', methods=['POST'])
def post_character():
    character = request.get_json()
    user_by_name = User.query.filter_by(name=character['name']).first()
   
    if not isinstance(character['name'], str) or len(character['name'].strip()) == 0:
         return({'error':'"name" must be a string'}), 400
    if user_by_name:
        if user_by_name.name == character['name']:
            return jsonify('This email is already used'), 403
    if not isinstance(character['gender'], str) or len(character['gender'].strip()) == 0:
         return({'error':'"gender" must be a string'}), 400
    if not isinstance(character['height'], str) or len(character['height'].strip()) == 0:
         return({'error':'"height" must be a string'}), 400
    if not isinstance(character['eye_color'], str) or len(character['eye_color'].strip()) == 0:
         return({'error':'"eye_color" must be a string'}), 400
    if not isinstance(character['skin_color'], str) or len(character['skin_color'].strip()) == 0:
         return({'error':'"skin_color" must be a string'}), 400
    if not isinstance(character['image'], str) or len(character['image'].strip()) == 0:
         return({'error':'"image" must be a string'}), 400

    character_created = Character(name=character['name'],gender=character['gender'],height=character['height'],eye_color=character['eye_color'],skin_color=character['skin_color'],image=character['image'])
    print(character_created)
    db.session.add(character_created)
    db.session.commit()
    return jsonify('Character added'), 200

# DELETE ONE CHARACTER / ELIMINAR UN PERSONAJE
@app.route('/character/<int:id>', methods=['DELETE'])
def delete_one_character(id):
    character = Character.query.filter_by(id=id).first()
    if character == None:
        return jsonify('character not found'), 404
    else:
        db.session.delete(character)
        db.session.commit()
        return jsonify('character deleted'), 200
    
# PLANETS
# GET PLANETS / OBTENER PLANETAS
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    if len(planets) == 0:
        return jsonify('no planets found'), 404
    else: 
        data_serialized = list(map(lambda planet: planet.serialize(), planets)) 
        return jsonify(data_serialized), 200

# GET ONE PLANET / OBTENER UN PLANETA
@app.route('/planet/<int:id>', methods=['GET'])
def get_one_planet(id):
    planet = Planet.query.filter_by(id=id).first()
    if planet == None:
        return jsonify('planet not found'), 404
    else:
        planet_serialized = planet.serialize()
        return jsonify(planet_serialized), 200

# POST PLANET / AÑADIR PLANETA
@app.route('/planet', methods=['POST'])
def post_planet():
    planet = request.get_json()
   
    if not isinstance(planet['name'], str) or len(planet['name'].strip()) == 0:
         return({'error':'"name" must be a string'}), 400
    if not isinstance(planet['population'], str) or len(planet['population'].strip()) == 0:
         return({'error':'"population" must be a string'}), 400
    if not isinstance(planet['diameter'], str) or len(planet['diameter'].strip()) == 0:
         return({'error':'"diameter" must be a string'}), 400

    planet_created = Planet(name=planet['name'],population=planet['population'],diameter=planet['diameter'])
    db.session.add(planet_created)
    db.session.commit()
    return jsonify('Planet added'), 200

# DELETE ONE PLANET / ELIMINAR UN PLANETA
@app.route('/planet/<int:id>', methods=['DELETE'])
def delete_one_planet(id):
    planet = Planet.query.filter_by(id=id).first()
    if planet == None:
        return jsonify('planet not found'), 404
    else:
        db.session.delete(planet)
        db.session.commit()
        return jsonify('planet deleted'), 200
    
# VEHICLES
# GET VEHICLES / OBTENER VEHICULOS
@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    if len(vehicles) == 0:
        return jsonify('no vehicles found'), 404
    else: 
        data_serialized = list(map(lambda vehicle: vehicle.serialize(), vehicles)) 
        return jsonify(data_serialized), 200

# GET ONE VEHICLE / OBTENER UN VEHICULO
@app.route('/vehicle/<int:id>', methods=['GET'])
def get_one_vehicle(id):
    vehicle = Vehicle.query.filter_by(id=id).first()
    if vehicle == None:
        return jsonify('vehicle not found'), 404
    else:
        vehicle_serialized = vehicle.serialize()
        return jsonify(vehicle_serialized), 200

# POST VEHICLE / AÑADIR VEHICULO
@app.route('/vehicle', methods=['POST'])
def post_vehicle():
    vehicle = request.get_json()
   
    if not isinstance(vehicle['name'], str) or len(vehicle['name'].strip()) == 0:
         return({'error':'"name" must be a string'}), 400
    if not isinstance(vehicle['model'], str) or len(vehicle['model'].strip()) == 0:
         return({'error':'"model" must be a string'}), 400
    if not isinstance(vehicle['size'], str) or len(vehicle['size'].strip()) == 0:
         return({'error':'"size" must be a string'}), 400

    vehicle_created = Vehicle(name=vehicle['name'],model=vehicle['model'],size=vehicle['size'])
    db.session.add(vehicle_created)
    db.session.commit()
    return jsonify('vehicle added'), 200

# DELETE ONE VEHICLE / ELIMINAR UN VEHICULO
@app.route('/vehicle/<int:id>', methods=['DELETE'])
def delete_one_vehicle(id):
    vehicle = Vehicle.query.filter_by(id=id).first()
    if vehicle == None:
        return jsonify('vehicle not found'), 404
    else:
        db.session.delete(vehicle)
        db.session.commit()
        return jsonify('vehicle deleted'), 200

# FAVORITES
# GET
# GET THE FAVORITES OF A USER / OBTENER FAVORITOS DE UN USUARIO
@app.route('/favorites/user/<int:user_id>', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify('user not found'), 404
    else:
        user_favorites = user.get_user_favorite()
        if len(user_favorites["favorites"]) == 0:
            return jsonify('no favorites found'), 404
        else: 
            return jsonify(user.get_user_favorite()), 200

# POST
# POST FAVORITE CHARACTER / AÑADIR PERSONAJE FAVORITO
@app.route('/favorite/user/character/<int:user_id>/<int:character_id>', methods=['POST'])
def post_favorite_character(user_id, character_id):
    user = User.query.filter_by(id=user_id).first()
    character = Character.query.filter_by(id=character_id).first()

    if user == None:
        return jsonify('user not found'), 404
    else:
        if character == None:
            return jsonify('character not found'), 404
        else:
            user_favorite_character_created = Favorite(user_id=user_id, character_id=character_id)
            db.session.add(user_favorite_character_created)
            db.session.commit()
            return jsonify('character added to user favorites'), 200

# POST FAVORITE PLANET / AÑADIR PERSONAJE PLANETA
@app.route('/favorite/user/planet/<int:user_id>/<int:planet_id>', methods=['POST'])
def post_favorite_planet(user_id, planet_id):
    user = User.query.filter_by(id=user_id).first()
    planet = Planet.query.filter_by(id=planet_id).first()

    if user == None:
        return jsonify('user not found'), 404
    else:
        if planet == None:
            return jsonify('planet not found'), 404
        else:
            user_favorite_planet_created = Favorite(user_id=user_id, planet_id=planet_id)
            db.session.add(user_favorite_planet_created)
            db.session.commit()
            return jsonify('planet added to user favorites'), 200

# POST FAVORITE VEHICLE / AÑADIR PERSONAJE VEHICULO
@app.route('/favorite/user/vehicle/<int:user_id>/<int:vehicle_id>', methods=['POST'])
def post_favorite_vehicle(user_id, vehicle_id):
    user = User.query.filter_by(id=user_id).first()
    vehicle = Vehicle.query.filter_by(id=vehicle_id).first()

    if user == None:
        return jsonify('user not found'), 404
    else:
        if vehicle == None:
            return jsonify('vehicle not found'), 404
        else:
            user_favorite_vehicle_created = Favorite(user_id=user_id, vehicle_id=vehicle_id)
            db.session.add(user_favorite_vehicle_created)
            db.session.commit()
            return jsonify('vehicle added to user favorites'), 200

# DELETE
# DELETE FAVORITE CHARACTER / ELIMINAR PERSONAJE FAVORITO
@app.route('/favorite/user/character/<int:user_id>/<int:character_id>', methods=['DELETE'])
def delete_one_character_favorite(user_id, character_id):
    favorite = Favorite.query.filter_by(user_id=user_id, character_id=character_id).first()
    if favorite == None:
        return jsonify('favorite not found'), 404
    else:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify('favorite deleted'), 200

# DELETE FAVORITE PLANET / ELIMINAR PLANETA FAVORITO
@app.route('/favorite/user/planet/<int:user_id>/<int:planet_id>', methods=['DELETE'])
def delete_one_planet_favorite(user_id, planet_id):
    favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite == None:
        return jsonify('favorite not found'), 404
    else:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify('favorite deleted'), 200
    
# DELETE FAVORITE VEHICLE / ELIMINAR VEHICULO FAVORITO
@app.route('/favorite/user/vehicle/<int:user_id>/<int:vehicle_id>', methods=['DELETE'])
def delete_one_vehicle_favorite(user_id, vehicle_id):
    favorite = Favorite.query.filter_by(user_id=user_id, vehicle_id=vehicle_id).first()
    if favorite == None:
        return jsonify('favorite not found'), 404
    else:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify('favorite deleted'), 200
    
# PUT CHARACTER / ACTUALIZAR PERSONAJE

# @app.route('/character<int:id>', methods=['PUT'])
# def put_character(id):
#     character = Character.query.filter_by(id=id).first()

#     if character == None:
#         return jsonify('character not found'), 404
#     else: 
#         character = request.get_json()
#         if not isinstance(character['name'], str) or len(character['name'].strip()) == 0:
#             return({'error':'"name" must be a string'}), 400
#         if not isinstance(character['gender'], str) or len(character['gender'].strip()) == 0:
#             return({'error':'"gender" must be a string'}), 400
#         if not isinstance(character['eye_color'], str) or len(character['eye_color'].strip()) == 0:
#             return({'error':'"eye_color" must be a list'}), 400

#         character_created = Character(name=character['name'],gender=character['gender'],eye_color=character['eye_color'])
#         print(character_created)
#         db.session.add(character_created)
#         db.session.commit()
#         return jsonify('Character added'), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
