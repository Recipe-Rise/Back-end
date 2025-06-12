from flask import request, jsonify, Response
from models import User ,db

ALLOWED_MIME_TYPES = [
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/webp',
    'image/bmp',
    'image/tiff',
    'image/x-icon',
]

def upload_image(user_id):
    data = request.files.get('image')
    if not data:
        return jsonify({'message': 'No image uploaded'}), 400

    # Optional: Validate MIME type
    if data.mimetype not in ALLOWED_MIME_TYPES:
        return jsonify({'message': 'Unsupported image format'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    # Read and store image binary
    image_binary = data.read()
    user.profile_photo = image_binary
    user.profile_mime = data.mimetype or 'image/jpeg'
    db.session.commit()
    return jsonify({
        'message': 'Image uploaded successfully'
    }), 200

def get_image(user_id):
    user = User.query.get(user_id)
    if user and user.profile_photo:
        return Response(
            user.profile_photo,
            mimetype=user.profile_mime,
            headers={
                "Content-Disposition": f"inline; filename=profile_image.{user.profile_mime.split('/')[-1]}"
            }
        )
    return jsonify({'message': 'No profile picture'}), 404