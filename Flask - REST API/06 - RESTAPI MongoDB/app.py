import json
from unicodedata import name
from unittest import result
from flask import Flask, jsonify, request
from flask_mongoengine import MongoEngine
import mongoengine as me
from marshmallow import Schema, fields

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    "db": "restapi",
}
db = MongoEngine(app)



class Framework(me.Document):
    name = db.StringField()

class FrameworkSchema(Schema):
    id = fields.Str(attribute="id")
    name = fields.Str()

@app.route('/')
def index():

    return "Hello World!"

# POST METHOD
@app.route("/api/frameworks/", methods=["POST"])
def add_framework():
    new_framework = Framework(name=request.json["name"])
    new_framework.save()

    framework_dict = {
        "id": "{}".format(new_framework.id),
        "name": new_framework.name
    }

    return jsonify(framework_dict)


# PUT METHOD
@app.route("/api/frameworks/<string:id>", methods=["PUT"])
def edit_framework(id):
    framework = Framework.objects(id=id).first()
    if not framework:
        return jsonify({'error': 'data not found'})
    else:
        framework.name = request.json["name"]
        framework.save()
        #framework.update(name=request.json["name"])
        framework_dict = {
            "id": f'{framework.id}',
            "name": framework.name
        }
        return jsonify(framework_dict)


# DELETE METHOD
@app.route('/api/frameworks/<string:id>', methods=["DELETE"])
def delete_framework(id):
    framework = Framework.objects(id=id).first()
    if not framework:
        return jsonify({'error': 'data not found'})
    else:
        framework.delete()
        return jsonify({"message": "ok"})


# GET METHOD
@app.route('/api/frameworks', methods=["GET"])
def get_all_frameworks():
    framework = Framework.objects()
    framework_schema = FrameworkSchema(many=True)
    results = framework_schema.dump(framework)
    
    return jsonify(results)


@app.route('/api/frameworks/<string:name>', methods=["GET"])
def get_framework_by_name(name):
    framework = Framework.objects(name=name).first()
    if not framework:
        return jsonify({'error': 'data not found'})
    else:
        framework_schema = FrameworkSchema()
        result = framework_schema.dump(framework)
        return (result)

