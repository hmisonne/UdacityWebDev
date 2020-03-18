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

# Get JWT https://fsnd-hm.auth0.com/authorize?audience=drink&response_type=token&client_id=d59ElIPjGrbgKfQzkJpasYUEkpXOFvzJ&redirect_uri=https://127.0.0.1:5000/login-results

# access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UTTJRVGsxT1VJME5rUTRRekZDUXpnM1FUUXlRMFEwUXpneE5UZERNVEl5TVVGRU1qVTFSZyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtaG0uYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNmQwYzc0MDg0NTcxMGM5MjIxMWQzMCIsImF1ZCI6ImRyaW5rIiwiaWF0IjoxNTg0NDY3NjY2LCJleHAiOjE1ODQ0NzQ4NjYsImF6cCI6ImQ1OUVsSVBqR3JiZ0tmUXprSnBhc1lVRWtwWE9GdnpKIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZHJpbmtzIiwiZ2V0OmRyaW5rcy1kZXRhaWwiLCJwYXRjaDpkcmlua3MiLCJwb3N0OmRyaW5rcyJdfQ.U0SpuA7AEpF2DvjNHR1mJ21Dif-HzLUhahW_l9mHMNqtDxZtBkQa5k338yRrftj4_pFPCWcU7ww0cM_wDvOfORh2piORWyoLpWwdhLmM96C7bMaZ3cL-XeZ8OEwv_iX0ShTQdW2A6fBbvd-8dwsbSMO4E6yyr9AMID2fSiiBp1W7fsCrlirROFNMec4bdCJAOL5iwmoFdyP21jF3XGDQXXyUt2FtEIBojWsqXLcCkLBFBUltN6gla90AZ9p9V40u8rxO9iJUfMWBTl1HWA9pByUZPMYyXab0MxFFeXszBmFHL17_qqYBi0wX-423l1n9m9crD_HwkT456RK_oxgoTQ
'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

## ROUTES


@app.route('/drinks', methods=['GET'])
def get_all_drinks():
    try:
        all_drink = Drink.query.all()
        drinks =[drink.short() for drink in all_drink]
        print(drinks)
        return jsonify({
            "success": True, 
            "drinks": drinks})
    except:
            abort(422)


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_details(payload):
    try:
        all_drink = Drink.query.all()
        drinks =[drink.long() for drink in all_drink]
        return jsonify({
            "success": True, 
            "drinks": drinks})
    except:
        abort(422)

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(payload):
    body = request.get_json()
    new_title = body.get('title', None)
    new_recipe = body.get('recipe', None)

    duplicate = Drink.query.filter(Drink.title == new_title).one_or_none()

    if duplicate != None:
        abort(400)

    try:
        new_drink = Drink(title=new_title,recipe=json.dumps([new_recipe]))
        new_drink.insert()
        return jsonify({
            "success": True, 
            "drinks": [new_drink.long()]})
    except:
        abort(422)


@app.route('/drinks/<drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def upate_drinks(token, drink_id):
    selected_drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

    if selected_drink == None:
        abort(404)
    
    body = request.get_json()

    try:
        new_title = body.get('title', None)
        new_recipe = body.get('recipe', None)

        if new_title != None:
            selected_drink.title = new_title
        if new_recipe != None:
            selected_drink.recipe = json.dumps(new_recipe)
        
        selected_drink.update()
        drink = selected_drink.long()
        return jsonify({
            "success": True, 
            "drinks": drink
            })
    except:
        abort(422)

@app.route('/drinks/<drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(token, drink_id):
    selected_drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

    if selected_drink == None:
        abort(404)
    try:
        selected_drink.delete()
        return jsonify({
        "success": True, 
        "delete": drink_id
        })
    except:
        abort(422)
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

@app.errorhandler(404)
def notfound(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "Internal Server Error"
      }), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "Bad request"
      }), 400

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
