from flask.views import MethodView
from flask_smorest import Blueprint, abort
#Hashing Algorithim
from passlib.hash import pbkdf2_sha256
#Access Token
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    jwt_required,
)

from db import db
from models import UserModel
from schemas import UserSchema
from blocklist import BLOCKLIST


blp = Blueprint("Users", "users", description="Operations on users")

#Register Class
@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        #Checks if Username is unique
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="A user with that username already exists.")

        user = UserModel(
            username=user_data["username"],
            #Hashes the Password to store in the Database
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        #Adds user to session
        db.session.add(user)
        #Pushes user to Database
        db.session.commit()

        return {"message": "User created successfully."}, 201

#Login Class
@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):

        #Checks if User Exists
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        #Verifies Password Using HASH - HASH Cannot be converted back to password, but part of it can be used to see if the password was used to 
        #Create it
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            #Creates Access Token and Refresh Token using User.ID 
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200


        abort(401, message="Invalid credentials.")

#Logout Class
@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200
    

@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        # Make it clear that when to add the refresh token to the blocklist will depend on the app design
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": new_token}, 200

@blp.route("/user/<int:user_id>")
class User(MethodView):
    """
    This resource can be useful when testing our Flask app.
    We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful
    when we are manipulating data regarding the users.
    """

    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200

