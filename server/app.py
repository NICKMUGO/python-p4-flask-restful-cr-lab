#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get():
        plants=Plant.query.all()
        db.session.add_all(plants)
        db.session.commit()
        plants_dict=[plant.to_dict() for plant in plants ]


        return make_response(jsonify(plants_dict), 200)
    
    def post():
        name=request.form.get("name")
        price=request.form.get("price")
        image=request.form.get("image")

        new_plant=Plant(
            name=name,
            price=float(price),
            image=image
        )
        try:
            db.session.add(new_plant)
            db.session.commit()
            return jsonify({"message": "New plant added successfully."}), 201
        except Exception as e:
            print(e)
            return jsonify({"error":"There was an error adding the plant"}),500
        
api.add_resource(Plants, '/plants')
class PlantByID(Resource):
    def get(id):
        plant=Plant.query.filter_by(id=id).first()
        db.session.add_all(plant)
        db.session.commit()
        plant_dict=plant.to_dict()
    
       
        return make_response(jsonify(plant_dict), 200)
        
api.add_resource(PlantByID, '/plants/<int:id>')
if __name__ == '__main__':
    app.run(port=5555, debug=True)
