from flask import Flask, request, jsonify, abort
app = Flask(__name__)


directories = []
def get_object(id):
    for obj in directories:
        if obj["id"] == id:
            return obj
    return None

def validate_object(obj):
    if not isinstance(obj, dict):
        return False
    if not "name" in obj or not isinstance(obj["name"], str):
        return False
    if not "emails" in obj or not isinstance(obj["emails"], list):
        return False
    for email in obj["emails"]:
        if not isinstance(email, str):
            return False
    return True

@app.route("/status/", methods=["GET"])
def status():
    return jsonify("pong")

@app.route("/directories/", methods=["GET"])
def get_directories():

    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 10))
 
    start = (page - 1) * page_size
    end = start + page_size
 
    results = directories[start:end]

    response = {
        "count": len(directories),
        "next": f"/directories/?page={page + 1}&page_size={page_size}" if end < len(directories) else None,
        "previous": f"/directories/?page={page - 1}&page_size={page_size}" if start > 0 else None,
        "results": results
    }
    return jsonify(response)


@app.route("/directories/", methods=["POST"])
def create_object():
   
    data = request.get_json()
  
    if not validate_object(data):
        abort(400) # Bad request
 
    data["id"] = len(directories) + 1
   
    directories.append(data)
   
    return jsonify(data), 201


@app.route("/directories/<int:id>/", methods=["GET"])
def get_object_by_id(id):

    obj = get_object(id)

    if not obj:
        abort(404)
 
    return jsonify(obj)


@app.route("/directories/<int:id>/", methods=["PUT"])
def update_object_by_id(id):

    obj = get_object(id)

    if not obj:
        abort(404)

    data = request.get_json()

    if not validate_object(data):
        abort(400) # Bad request

    obj["name"] = data["name"]
    obj["emails"] = data["emails"]
  
    return jsonify(obj)


@app.route("/directories/<int:id>/", methods=["PATCH"])
def patch_object_by_id(id):
  
    obj = get_object(id)
    
    if not obj:
        abort(404)
    
    data = request.get_json()
   
    if not isinstance(data, dict):
        abort(400) # Bad request

    if "name" in data and isinstance(data["name"], str):
        obj["name"] = data["name"]
    if "emails" in data and isinstance(data["emails"], list):
        for email in data["emails"]:
            if not isinstance(email, str):
                abort(400) # Bad request
        obj["emails"] = data["emails"]
    
    return jsonify(obj)

# Ruta para eliminar un objeto por id
@app.route("/directories/<int:id>/", methods=["DELETE"])
def delete_object_by_id(id):
  
    obj = get_object(id)
 
    if not obj:
        abort(404)
  
    directories.remove(obj)
 
    return "", 204
