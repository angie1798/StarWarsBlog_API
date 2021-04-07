"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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

#get all users
@app.route('/user', methods=['GET'])
def get_user():
    user_query= User.query.all()
    all_user= list(map(lambda x: x.serialize(), user_query))
    return jsonify(all_user),200

#get all people
@app.route('/people', methods=['GET'])
def get_people():
    people_query= People.query.all()
    all_people= list(map(lambda x: x.serialize(), people_query))
    return jsonify(all_people),200

#get all planets
@app.route('/planet', methods=['GET'])
def get_planet():
    planet_query= Planet.query.all()
    all_planet = list(map(lambda x: x.serialize(), planet_query))
    return jsonify(all_planet),200

#get all favorites related to an specific user
@app.route('/user/<int:id>/favorite', methods=['GET'])
def get_fav(id):
    query= User.query.get(id)
    if query is None:
        return("this is not fine")
    else:
        result= Favorite.query.filter_by(user_id= query.id)
        lista = list(map(lambda x: x.serialize(), result))
        return jsonify(lista),200

#get an specific character from people
@app.route('/people/<int:id>', methods=['GET'])
def get_peopleid(id):
    personid = People.query.get(id)
    result= personid.serialize()
    return jsonify(result), 200

#get an specific planet
@app.route('/planet/<int:id>', methods=['GET'])
def get_planetid(id):
    planetid = Planet.query.get(id)
    result= planetid.serialize()
    return jsonify(result), 200

#add a favorite to an specific user
@app.route('/user/<int:userid>/favorite', methods=['POST'])
def post_fav(userid):
    req = request.get_json()
    fav = Favorite(user_id=userid, planet_id=req["planet_id"], person_id=req["person_id"])
    db.session.add(fav)
    db.session.commit()
    return("Todo correcto")

#delete an specific favorite
@app.route('/favorite/<int:favid>', methods=['DELETE'])
def del_fav(favid):
    fav = Favorite.query.get(favid)
    if fav is None:
        raise APIException('Favorite not found', status_code=404)
    db.session.delete(fav)
    db.session.commit()
    return ("Elemento eliminado")

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
