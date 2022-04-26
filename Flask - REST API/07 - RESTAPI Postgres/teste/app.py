from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:123456@localhost:5432/my_db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Pessoa(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cidade = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return self.nome

    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class RecipeSchema(Schema):
    id = fields.Integer()
    nome = fields.String()
    cidade = fields.String()


@app.route('/')
def index():
    return "Hello World!"


@app.route('/pessoas', methods=['GET'])
def get_all_pessoa():
    pessoas = Pessoa.get_all()

    serializer = RecipeSchema(many=True)

    data = serializer.dump(pessoas)

    return jsonify(
        data
    )


@app.route('/pessoas', methods=['POST'])
def create_a_pessoa():
    data = request.get_json()

    new_pessoa = Pessoa(
        nome = data.get('nome'),
        cidade = data.get('cidade')
    )

    new_pessoa.save()

    serializer = RecipeSchema()

    data = serializer.dump(new_pessoa)

    return jsonify(
        data
    ), 201

@app.route('/pessoas/<int:id>', methods=['PUT'])
def update_pessoa(id):
    pessoa_to_update = Pessoa.get_by_id(id)

    data = request.get_json()

    pessoa_to_update.nome = data.get('nome')
    pessoa_to_update.cidade = data.get('cidade')

    db.session.commit()

    serializer = RecipeSchema()

    pessoa_data = serializer.dump(pessoa_to_update)

    return jsonify(pessoa_data), 200

@app.route('/pessoas/<int:id>', methods=['DELETE'])
def delete_pessoa(id):
    pessoa_to_delete = Pessoa.get_by_id(id)

    pessoa_to_delete.delete()

    return jsonify({"message": "Deleted"}), 204


# from app import Pessoa, db
# db.create_all()

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=4000)