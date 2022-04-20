from flask import Flask, jsonify, request

app = Flask(__name__)

frameworks = [
    {
        "id": 1,
        "name": "Flask"
    },
    {
        "id": 2,
        "name": "ExpressJS"
    },
    {
        "id": 3,
        "name": "Laravel"
    }
]


@app.route('/')
def index():

    return "Hello World!"


@app.route('/api/frameworks', methods=["GET"])
def get_frameworks():

    return jsonify(frameworks)


@app.route('/api/frameworks/<string:name>', methods=["GET"])
def get_framework_by_name(name):
    framework = []
    for i in frameworks:
        if i["name"] == name:
            framework.append(i)

    return jsonify(framework)


@app.route('/api/frameworks/', methods=["POST"])
def add_framework():
    framework = {
        "id": request.json["id"],
        "name": request.json["name"]
    }
    frameworks.append(framework)

    return jsonify(frameworks) 

# PUT
@app.route('/api/frameworks/<int:id>', methods=["PUT"])
def edit_framework(id):
    framework = [framework for framework in frameworks if framework["id"] == id]
    
    framework[0]["id"] = int(request.json["id"])
    framework[0]["name"] = request.json["name"] 

    return jsonify(framework)


if __name__ == "__main__":
    app.run(debug=True)