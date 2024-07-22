#music v2/backend/Mysite/auth.py
import os
from flask import Blueprint,request,jsonify,current_app
from . import db
from .model import User, Role
from werkzeug.security import check_password_hash 
from werkzeug.utils import secure_filename
from flask_jwt_extended import create_access_token, create_refresh_token,decode_token,jwt_required,unset_jwt_cookies
from datetime import datetime, timedelta
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func

#..................................................User/creator_portion..................................................


auth = Blueprint("auth",__name__)



# Function to generate JWT token
def generate_token(user_id, user_role,user_username):
    token =create_access_token(
                identity=user_id,
                additional_claims={'role': user_role, 'username': user_username},
               
            )
   
    return token

# Function to generate JWT refresh token
def generate_refresh_token(user_id,user_role,user_name):
    
    refresh_token = create_refresh_token(
                        identity=user_id,
                        additional_claims={'role': user_role, 'username': user_name},
                        
                    )
    return refresh_token

# Refresh token endpoint
@auth.route('/refresh-token', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
   
        refresh_token = request.json.get('refresh_token')
        # print(refresh_token)

        # Verify the refresh token
        payload = decode_token(refresh_token)
        # print(payload)
        user_id = payload['sub']
        user_role = payload['role']
        user_name = payload['username']

        # Generate a new access token
        access_token = generate_token(user_id,user_role,user_name)

        return jsonify({'access_token': access_token})
    
    



# Login api  route
@auth.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        data = request.json
        login_identifier = data.get("username")
        password = data.get("password")

        # Check if login_identifier is email or username
        user = User.query.filter((User.email == login_identifier) | (User.username == login_identifier)).first()

        if user and check_password_hash(user.password, password) and user.role.name == 'Admin':
            user.last_login = datetime.now()
            db.session.commit()
            # Generate tokens
            access_token = generate_token(user.id, user.role.name,user.username)
            refresh_token = generate_refresh_token(user.id, user.role_id,user.username)
            username = user.username

            return jsonify({
                'access_token': access_token,
                'refresh_token': refresh_token,
                'username' : username
            })
        else:
            return jsonify({'message': 'Invalid credentials'}),400
    else:
        # Handle GET request (e.g., render login form)
        return jsonify({'message': 'This endpoint supports only POST requests for login.'})
    
@auth.route("/other_login", methods=["POST"])
def other_login():
    if request.method == "POST":
        data = request.json
        login_identifier = data.get("username")
        password = data.get("password")

        # Check if login_identifier is email or username
        user = User.query.filter((User.email == login_identifier) | (User.username == login_identifier)).first()

        if user and check_password_hash(user.password, password) and (user.role.name == 'User' or user.role.name == 'Creator'):
            user.last_login = datetime.now()
            db.session.commit()
            # Generate tokens
            access_token = generate_token(user.id, user.role.name,user.username)
            refresh_token = generate_refresh_token(user.id, user.role_id,user.username)
            username = user.username

            return jsonify({
                'access_token': access_token,
                'refresh_token': refresh_token,
                'username' : username
            })
        else:
            return jsonify({'message': 'Invalid credentials'}), 400
    else:
        # Handle GET request (e.g., render login form)
        return jsonify({'message': 'This endpoint supports only POST requests for login.'})
    



@auth.route("/signup",methods=["GET","POST"])
def sign_up():
    
        image_data = request.files["image"]
        email =request.form.get("email")
        name = request.form.get("name")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        role_name = request.form.get("role_name")  

        # Validate form data
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        upload_folder =current_app.config['UPLOAD_FOLDER']
        user_upload_folder = os.path.join(upload_folder, 'User')

        if email_exists:
            return jsonify({"message": "Email is already in use"})
        elif username_exists:
            return jsonify({"message": "Username is already in use"})
        elif password1 != password2:
            return jsonify({"message": "Passwords don't match"})
        elif len(password1) < 6:
            return jsonify({"message": "Password must be at least 6 characters long"})
        elif len(username) < 3:
            return jsonify({"message": "Username is too short"})
        elif not name:
            return jsonify({"message":"A name required"})
        elif not image_data:
            return jsonify({"message": "No image selected"})
        else:
            # Find the role ID based on the role name
            role = Role.query.filter(func.lower(Role.name) == func.lower(role_name)).first()

            if not role:
                return jsonify({"message": "Role not found"})

          
            

            timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
            filename = f"{secure_filename(image_data.filename)}_{timestamp}"
            filepath = os.path.join(user_upload_folder, filename)
            image_data.save(filepath)

            # Create a new user instance
            new_user = User(
                image=filepath,
                name=name,
                email=email,
                username=username,
                role_id=role.id  
            )

            new_user.set_password(password1)
            db.session.add(new_user)
            db.session.commit()

            return jsonify({"message": "User created successfully"})

    


# #edit profile
# @auth.route("/edit-profile", methods=["POST"])
# @login_required
# def edit_profile():
#     data = request.get_json()

#     if data:
#         user = current_user
#         user.name = data.get("name", user.name)
#         user.email = data.get("email", user.email)
#         user.username = data.get("username", user.username)

#         # Check if the image is updated
#         image_data = data.get("image")
#         if image_data:
#             encoded_image = encode_image_to_base64(image_data)
#             user.image = encoded_image
#             user.mimetype_profile = image_data.get("mimetype")

#         # Update the user in the database
#         db.session.commit()

#         return jsonify({"message": "Profile updated successfully"})

#     return jsonify({"message": "Invalid data received"})


# from flask import request, jsonify
# from werkzeug.security import check_password_hash, generate_password_hash

# @auth.route("/change-password", methods=["POST"])
# @login_required
# def change_password():
#     data = request.get_json()

#     if data:
#         current_password = data.get("current_password")
#         new_password = data.get("new_password")
#         confirm_password = data.get("confirm_password")

#         # Check if all required fields are provided
#         if not all([current_password, new_password, confirm_password]):
#             return jsonify({"message": "All fields are required"}), 400

#         # Check if the new password matches the confirmation
#         if new_password != confirm_password:
#             return jsonify({"message": "New password and confirmation password do not match"}), 400

#         # Verify the current password
#         user = current_user
#         if not check_password_hash(user.password, current_password):
#             return jsonify({"message": "Current password is incorrect"}), 400

#         # Update the password
#         user.password = generate_password_hash(new_password, method="sha256")
#         db.session.commit()

#         return jsonify({"message": "Password changed successfully"}), 200

#     return jsonify({"message": "Invalid data received"}), 400


@auth.route("/logout")
@jwt_required()
def logout():
    try:
        # Perform logout actions
        unset_jwt_cookies()  # Clear JWT cookies
        return jsonify({"message": "Logout successful"})
    except Exception as e:
        # Handle any exceptions that might occur during logout
        return jsonify({"error": str(e)})
