from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():

    return "Hello World!"

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

@app.route("/api/frameworks/", methods=["GET"])
def get_frameworks():

    return jsonify(frameworks)


@app.route('/api/frameworks/', methods=["POST"])
def add_framework():
    # framework = request.json
    # tratando anomalias 
    framework = {
        "id": request.json["id"],
        "name": request.json["name"]
    }
    frameworks.append(framework)

    return jsonify(frameworks)


if __name__ == "__main__":
    app.run(debug=True)