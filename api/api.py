### Ski Resort API

# libraries
from flask import Flask, jsonify, abort, request, make_response, url_for, redirect
from werkzeug.exceptions import HTTPException
import json

# Initialize app
app = Flask(__name__)

# JSON data pattern example
'''{
    "elevation": "2319m",
    "name": "big white",
    "city": "kelowna"
  }'''

# JSONify error codes
@app.errorhandler(HTTPException)
def handle_exception(e):
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

# GET all areas
@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('get_areas'))

@app.route('/areas', methods=['GET'])
def get_areas():
    jsonfile = open('./data.json', 'r')
    file_data = json.loads(jsonfile.read())
    jsonfile.close()
    return json.dumps(file_data)

# GET specific area
@app.route('/areas/<name>', methods=['GET'])
def get_area(name):
    jsonfile = open('./data.json', 'r')
    file_data = json.loads(jsonfile.read())
    jsonfile.close()
    for area in file_data:
        if str(name) == area["name"]:
            return jsonify(area)
    # Requested URL doesn't exist in JSON file
    else:
        abort(404)

# POST (create) area
@app.route('/areas', methods=['POST'])
def create_area():
    # Check post datatype
    if not request.get_json():
        abort(400)
    else:
        post = request.get_json()
        # Check keys are correct
        if "name" and "city" and "elevation" in post:
            values = post.values()
            # Check key-value pairs aren't empty
            for val in values:
                if val == '':
                    abort(400)
            # Make sure name entry doesn't exist already
            jsonfile = open('./data.json', 'r')
            file_data = json.loads(jsonfile.read())
            jsonfile.close()
            for area in file_data:
                if area['name'] == post['name']:
                    print(area['name'])
                    abort(400)
                # Append to JSON file
                else:
                    file_data.append(post)
                    jsonfile = open('./data.json', 'w')
                    json.dump(file_data, jsonfile)
                    jsonfile.close()
                    return jsonify(post), 201
        else:
            abort(400)

# PUT (create / modify) specific area
@app.route('/areas/<name>', methods = ['PUT'])
def modify_area(name):
    # Check post datatype
    if not request.get_json():
        abort(400)
    else:
        put = request.get_json()
        # Check keys are correct
        if "name" and "city" and "elevation" in put:
            values = put.values()
            # Check key-value pairs aren't empty
            for val in values:
                if val == '':
                    abort(400)
            # Check if name entry exists
            jsonfile = open('./data.json', 'r')
            file_data = json.loads(jsonfile.read())
            jsonfile.close()
                # Modify selected area
            for i, area in enumerate(file_data):
                if area['name'] == str(name):
                    file_data[i] = put
                # Submit changes to JSON
                    jsonfile = open('./data.json', 'w')
                    json.dump(file_data, jsonfile)
                    jsonfile.close()
                    return jsonify(put)
            # Add entry to JSON if it doesn't already exist
            else:
                file_data.append(put)
                jsonfile = open('./data.json', 'w')
                json.dump(file_data, jsonfile)
                jsonfile.close()
                return jsonify(put), 201
        else:
            abort(400)

# DELETE specific area
@app.route('/areas/<name>', methods = ['DELETE'])
# Check delete datatype
def delete_area(name):
    if not request.get_json():
        abort(400)
    # Check that contents of delete request match the url route
    delete = request.get_json()
    if delete["name"] == str(name):
        jsonfile = open('./data.json', 'r')
        file_data = json.loads(jsonfile.read())
        jsonfile.close()
        print(file_data)
        # check that delete request matches one of the JSON objects & delete
        for i, area in enumerate(file_data):
            if area['name'] == str(name):
                file_data.pop(i)
                jsonfile = open('./data.json', 'w')
                json.dump(file_data, jsonfile)
                jsonfile.close()
                return jsonify(delete)
        else:
            abort (404)
    else:
        abort (400)

# Run app
if __name__ == '__main__':
    app.run(debug='true')
