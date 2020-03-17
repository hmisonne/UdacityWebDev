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

# https://fsnd-hm.auth0.com/authorize?audience=drink&response_type=token&client_id=d59ElIPjGrbgKfQzkJpasYUEkpXOFvzJ&redirect_uri=https://127.0.0.1:5000/login-results

# access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UTTJRVGsxT1VJME5rUTRRekZDUXpnM1FUUXlRMFEwUXpneE5UZERNVEl5TVVGRU1qVTFSZyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtaG0uYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNmQwYzc0MDg0NTcxMGM5MjIxMWQzMCIsImF1ZCI6ImRyaW5rIiwiaWF0IjoxNTg0NDUzOTg1LCJleHAiOjE1ODQ0NjExODUsImF6cCI6ImQ1OUVsSVBqR3JiZ0tmUXprSnBhc1lVRWtwWE9GdnpKIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZHJpbmtzIiwiZ2V0OmRyaW5rcy1kZXRhaWwiLCJwYXRjaDpkcmlua3MiLCJwb3N0OmRyaW5rcyJdfQ.H_XaGQaj8FRaBfvOvyHQFIwg2mwKQFgOmgujlcn4vxQ-WNz4OsXubhCmoakAvj7v6Ymc8SsYMGdVmvp5vGEF5GFp1O341QhVRQORPnVMMu0M4Zfb553CsRpBcPZV7NpRFabG0ZyO9HEAgpw0dAM2eVc3wlp_cC-QU0Ysg6c6lEkxA5E2xQEetUnq_cUuyiyQSVAZ248AA2Rx_B-XZmg5CjFuCTsbid0LkGI1xIvHzs2qWsrhXCExj8SpHyaPyp4UQZ1mgS-QEhACngAOwh_u4TAE0Rl5EFQDKToRYgupL8RKTdppwEVtIOJ03B89_2FiDrRp7JN_8n8yHr4LpikPJA

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_all_drinks():
    all_drink = Drink.query.all()
    drinks = []
    for drink in all_drink:
        drinks.append(drink.short())
    return jsonify({
        "success": True, 
        "drinks": drinks})

@app.route('/')
def index():
    return 'Hello'

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_details(payload):
    print(payload)
    all_drink = Drink.query.all()
    drinks = []
    for drink in all_drink:
        drinks.append(drink.long())
    return jsonify({
        "success": True, 
        "drinks": drinks})

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink():
    body = request.get_json()
    new_title = body.get('title', None)
    new_recipe = body.get('recipe', None)
    try:
        drink = Drink(title=new_title,recipe=new_recipe)
        drink.insert()
        return jsonify({
            "success": True, 
            "drinks": drink})
    except:
        abort(422)

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def upate_drinks(id):
    selected_drink = Drink.query.filter(Drink.id == id).one_or_none()

    if selected_drink == None:
        abort(404)
    
    body = request.get_json()
    new_title = body.get('title', None)
    new_recipe = body.get('recipe', None)

    selected_drink.title = new_title
    selected_drink.recipe = new_recipe
    
    selected_drink.update()
    drink = selected_drink.long()
    return jsonify({
        "success": True, 
        "drinks": drink
        })

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(id):
    selected_drink = Drink.query.filter(Drink.id == id).one_or_none()

    if selected_drink == None:
        abort(404)
    selected_drink.delete()
    return jsonify({
    "success": True, 
    "delete": id
    })
## Error Handling
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

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@app.errorhandler(404)
def notfound(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404
'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
