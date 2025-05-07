from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'your_default_secret_key'
    DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1', 't']
    AI_MODEL = os.getenv('AI_MODEL') or 'gpt-3.5-turbo'
    API_KEY = os.getenv('API_KEY') or 'your_api_key_here'
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    DATABASE_URI = os.getenv('DATABASE_URI') or 'sqlite:///site.db'