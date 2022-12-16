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
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
# db_drop_and_create_all(app)

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


class DBConstraintError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code
        # print(f'constraint error is {error} and code is {status_code} ')


@app.route('/drinks')
def drinks():
    # try:
    # print('GETTING ALL DRINKS')
    drinks = Drink.query.order_by(Drink.id).all()
    # print(f' drink 1 is {drinks[0].short()} its a {type(drinks[0].short())}')

    drinks = [drink.short() for drink in drinks]
    # print(f'all drinks {drinks}')

    return jsonify(
        {
            'success': True,
            'drinks': drinks
        }
    )
    # except Exception as e:
    #     print(e)
    #     abort(500)


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def drink_details(jwt):
    print('GETTING ALL DRINK DETAILS')
    try:
        # print(f'details token: {jwt}')
        drinks = Drink.query.order_by(Drink.id).all()
        drinks = [drink.long() for drink in drinks]

        return jsonify(
            {
                "success": True,
                "drinks": drinks
            }
        )
    except:
        abort(500)


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
def add_drink(jwt):
    # print(f'jwt {jwt}')
    body = request.get_json()
    if 'title' and 'recipe' not in body:
        abort(422)

    # print(f'recipe  {body.get("recipe")}  {type(body.get("recipe"))}')
    new_title = body.get('title')
    new_recipe = json.dumps(body.get('recipe'))

    # print(f'new_recipe {new_recipe} type {type(new_recipe)}')

    try:
        drink = Drink(
            title=new_title,
            recipe=new_recipe
        )

        drink.insert()
        new_drink = [Drink.query.get(drink.id).long()]

        return jsonify(
            {
                'success': True,
                'drinks': new_drink
            }
        )
    except Exception as e:
        if 'constraint failed' in e.args[0]:
            raise DBConstraintError({
                'code': 'database_constraint_failed',
                "message": e.args[0]
            }, 422)
        else:
            print(f'error in add drink {e}')
            abort(500)


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


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(jwt, *args, id):
    if not id:
        abort(400)
    
    drink = Drink.query.get(id)
    if not drink:
        abort(404)
    req = request.get_json()
    name_edit = req.get('title', None)
    recipe_edit = json.dumps(req.get('recipe', None))
    if name_edit:
        drink.title = name_edit
    if recipe_edit:
        drink.recipe = recipe_edit
    if not name_edit and not recipe_edit:
        abort(400)
    try:

        drink.update()

        return jsonify({
            "success": True,
            "drinks": drink.long()
        })
    except Exception as e:
        if 'constraint failed' in e.args[0]:
            raise DBConstraintError({
                'code': 'database_constraint_failed',
                "message": e.args[0]
            }, 422)
        else:
            print(f'error in patch drink {e}')
            abort(500)


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


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(jwt, *args, id):
    if not id:
        abort(400)
    drink = Drink.query.get(id)
    if not drink:
        abort(404)
    try:
        drink.delete()

        return jsonify(
            {
                "success": True,
                "delete": id
            }
        )
    except:
        abort(500)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    # print(error)
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
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "forbidden"
    }), 403


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
    }), 405


@app.errorhandler(500)
def internal_server_err(error):
    # print(f'ERROR {error}')
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
    }), 500


@app.errorhandler(AuthError)
def auth_error(e):
    return jsonify({
        "success": False,
        "error": e.status_code,
        "message": e.error
    }), 401


@app.errorhandler(DBConstraintError)
def unprocessable(e):
    return jsonify({
        "success": False,
        "error": e.status_code,
        "message": e.error
    }), 422


'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
    
'''
'''

|￣￣￣￣￣￣￣ |  
|    Hello    |
|_____________|
(\__/) || 
(•ㅅ•) || 
/    づ




'''
