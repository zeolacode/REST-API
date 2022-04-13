from flask import Flask, jsonify

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

@app.route("/api/frameworks/", methods=["GET"])
def get_frameworks():

    return jsonify(frameworks)

@app.route('/api/frameworks/<string:name>')
def get_framework_by_name(name):
    framework = []
    for i in frameworks:
        if i["name"] == name:
            framework.append(i)
    
    return jsonify(framework[0])

@app.route('/api/frameworks/<int:id>')
def get_framework_by_id(id):
    framework = []
    for i in frameworks:
        if i["id"] == id:
            framework.append(i)
    
    return jsonify(framework[0])


if __name__ == "__main__":
    app.run(debug=True)