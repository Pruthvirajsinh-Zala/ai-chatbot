class UserInteraction:
    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message

class ChatbotResponse:
    def __init__(self, response_id, response_text):
        self.response_id = response_id
        self.response_text = response_text

class Conversation:
    def __init__(self, conversation_id):
        self.conversation_id = conversation_id
        self.interactions = []

    def add_interaction(self, user_interaction, chatbot_response):
        self.interactions.append((user_interaction, chatbot_response))