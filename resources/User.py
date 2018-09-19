from flask import request ,render_template
from flask_restful import Resource
from Model import db,User, UserSchema


users_schema = UserSchema(many =True)
user_schema = UserSchema() 


def validate_keys(available_keys,actual_keys):
    for k in actual_keys:
        if k not in available_keys.keys():
            return True
    return False


class UserResource(Resource):
    def get(self):
        users = User.query.all()
        print(users)
        print(dir(users[0]))
        print("---"*30)
        user = users_schema.dump(users)
        # return render_template('base.html')
        return {'status': 'success', 'data': user}, 200

    def post(self):
        json_data = request.get_json(force=True)
        print(json_data)
        actual_keys = ['email','password','username']
        if validate_keys(json_data,actual_keys):
            return {'message':'key is missing'}
        if not User.isValidEmail(**json_data):
            return {'message': 'No input data provided'}, 400
        users = User.query.filter_by(email=json_data['email']).first()
        if users:
            return {'message': 'Category already exists'}, 400
        users = User(email=json_data['email'],password=json_data['password'],username=json_data['password'])
        db.session.add(users)
        db.session.commit()
        result = user_schema.dump(users)
        return { "status": 'success', 'data': result }, 201

    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        user = User.query.filter_by(id=data['id']).first()
        if not user:
            return {'message': 'Category does not exist'}, 400
        user.name = json_data['name']
        db.session.commit()
        result = user_schema.dump(user)
        return { "status": 'success', 'data': result }, 204

        
    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400

        user = User.query.filter_by(id=data['id']).delete()
        db.session.commit()

        result = user_schema.dump(user)

        return { "status": 'success', 'data': result}, 204
