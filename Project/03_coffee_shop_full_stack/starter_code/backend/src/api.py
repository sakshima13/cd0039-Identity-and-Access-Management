import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
!! Running this funciton will add one
'''
# db_drop_and_create_all()

# ROUTES
'''
GET /drinks
'''


@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.all()
    if drinks is None:
        abort(404)

    print('d', drinks)
    try:
        data = jsonify({
            "success": True,
            "drinks": [drink.short() for drink in drinks]
        })
        return data, 200
    except:
        abort(404)


'''
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_details(jwt):
    drinks = Drink.query.all()
    if drinks is None:
        abort(404)

    print('dd', drinks)
    try:
        data = jsonify({
            "success": True,
            "drinks": [drink.long() for drink in drinks]
        })
        return data, 200
    except:
        abort(404)


'''
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drinks(jwt):
    req_body = request.get_json()
    recipe = req_body.get('recipe'),
    title = req_body.get('title')

    if type(recipe) is dict:
        recipe = [recipe]

    drinks = Drink(title=title, recipe=json.dumps(recipe))

    try:
        drinks.insert()
        data = jsonify({
            "success": True,
            "drinks": [drinks.long()]
        })
        return data, 200
    except:
        abort(404)


'''
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('post:drinks')
def edit_drink(jwt, id):
    req_body = request.get_json()
    recipe = req_body.get('recipe'),
    title = req_body.get('title')

    selected_drink = Drink.query.filter(Drink.id == id).one_or_none()

    if selected_drink is None or selected_drink.title != title:
        abort(404)

    if type(recipe) is dict:
        recipe = [recipe]

    try:
        selected_drink.update()
        data = jsonify({
            "success": True,
            "drinks": [selected_drink.long()]
        })
        return data, 200
    except:
        abort(404)


'''
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, id):
    selected_drink = Drink.query.filter(Drink.id == id).one_or_none()

    if selected_drink is None:
        abort(404)

    try:
        selected_drink.delete()
        data = jsonify({
            "success": True,
            "drinks": [selected_drink.long()]
        })
        return data, 200
    except:
        abort(404)


# Error Handling
'''
Example error handling for unprocessable entity
'''

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad Request'
    }), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'Unauthorized'
    }), 401

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal Server Error'
    }), 500

@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        'success': False,
        'error': error.error['code'],
        'message': error.error['description']
    }), error.status_code