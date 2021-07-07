from flask_restful import Resource
from flask import jsonify, request
from app.services import user_profile_service


class UserProfileAPI(Resource):
    def get(self):
        return jsonify(user_profile_service.get_user_profiles(**request.args))

    def post(self):
        user_profile_dict = request.get_json()
        return jsonify(user_profile_service.create_user_profile(user_profile_dict))

    def put(self):
        user_profile_dict = request.get_json()
        return jsonify(user_profile_service.update_user_profile(user_profile_dict))


class SingleUserProfileAPI(Resource):
    def get(self, username):
        return jsonify(user_profile_service.get_user_profile(username))

    def delete(self, username):
        return jsonify(user_profile_service.delete_user_profile(username))
