from flask import Blueprint, request, jsonify, render_template

main = Blueprint('main', __name__)

@main.route('/')
def home():
    # Render the main page with a "New Chat" button
    return render_template('index.html')  # Add 'return' here

@main.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    # Process the user input and generate a response
    response = generate_chatbot_response(user_input)
    return jsonify({'response': response})

def generate_chatbot_response(user_input):
    # Placeholder for chatbot response logic
    return f"This is a placeholder response to: {user_input}"