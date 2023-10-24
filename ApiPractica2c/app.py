from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://cnp2_user:my_cool_secret_2@postgres-db:5432/cnp2_database'
db = SQLAlchemy(app)

class Directory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    emails = db.Column(db.ARRAY(db.String(100)))

@app.route("/status/", methods=["GET"])
def status():
    return jsonify("pong")

@app.route("/directories/", methods=["GET"])
def get_directories():
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 10))

    start = (page - 1) * page_size
    end = start + page_size

    directories = Directory.query.offset(start).limit(page_size).all()

    response = {
        "count": Directory.query.count(),
        "next": f"/directories/?page={page + 1}&page_size={page_size}" if end < Directory.query.count() else None,
        "previous": f"/directories/?page={page - 1}&page_size={page_size}" if start > 0 else None,
        "results": [
            {"id": directory.id, "name": directory.name, "emails": directory.emails}
            for directory in directories
        ]
    }
    return jsonify(response)

@app.route("/directories/", methods=["POST"])
def create_directory():
    data = request.get_json()

    if not validate_object(data):
        abort(400)  # Bad request

    directory = Directory(name=data["name"], emails=data["emails"])
    db.session.add(directory)
    db.session.commit()

    return jsonify({"id": directory.id, "name": directory.name, "emails": directory.emails}), 201

# Resto de las rutas...

if __name__ == "__main__":
    app.run()
