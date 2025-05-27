from flask import Blueprint, request, jsonify, render_template
import google.generativeai as genai
from app.models import db, Message
import os

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

main = Blueprint('main', __name__)

@main.route('/')
def home():
    messages = Message.query.order_by(Message.timestamp).all()
    return render_template('index.html', messages=messages)

@main.route('/api/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')

    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    user_message = Message(text=user_input, is_user=True)
    db.session.add(user_message)
    db.session.commit()

    try:
        response = model.generate_content(user_input).text
    except Exception as e:
        response = f"An error occurred: {e}"

    bot_message = Message(text=response, is_user=False)
    db.session.add(bot_message)
    db.session.commit()
    return jsonify({'response': response})