from flask import request, jsonify, Response
from models import User ,db

def upload_image(user_id):
    data = request.files.get('image')
    user = User.query.get(user_id)

    # Read the image as binary and store in DB
    image_binary = data.read()
    user.profile_photo = image_binary
    user.profile_mime = data.mimetype

    db.session.commit()
    return jsonify({
        'message': 'image uploaded successfully',
    }), 200

def get_image(user_id):
    user = User.query.get(user_id)
    if user and user.profile_photo:
        return Response(user.profile_photo, mimetype=user.profile_mime)

    return jsonify({
        "No profile picture"
    }), 404