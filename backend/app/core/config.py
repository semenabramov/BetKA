import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Настройки базы данных
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://root:mysql@localhost/betka')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Настройки сервера
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true' 