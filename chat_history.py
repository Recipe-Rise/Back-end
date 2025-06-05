from flask import request, jsonify
from datetime import datetime
from models import Chat ,db


def add_chat_buble(user_id):

    data = request.form.to_dict()
    if not data["chat_buble"] or not data["sender"] :
        return jsonify({'message': 'Data missing'}),400
    new_chat_buble = Chat(
        user_id = user_id,
        chat_buble = data["chat_buble"],
        sender = data["sender"],
        time_and_date = datetime.now()
    )
    db.session.add(new_chat_buble)
    db.session.commit()

    return jsonify({
        'message': 'chat buble added successfully',
        'user_id': user_id,
        'chat_buble': new_chat_buble.chat_buble,
        "sender": new_chat_buble.sender,
        'time_and_date': new_chat_buble.time_and_date,
    }), 201


def get_chat_bubbles(user_id):
    try:
        # Retrieve all chat bubbles for the specified user_id
        chat_bubbles = Chat.query.filter_by(user_id=user_id).all()
        if not chat_bubbles:
            return jsonify({"message": "No chat bubbles found for this user."}), 404
        # Convert the result to a list of dictionaries
        result = []
        for bubble in chat_bubbles:
            result.append({
                "buble_id": bubble.buble_id,
                "user_id": bubble.user_id,
                "chat_buble": bubble.chat_buble,
                "sender": bubble.sender,
                "time_and_date": bubble.time_and_date.isoformat()  # Format the datetime if needed
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    #return