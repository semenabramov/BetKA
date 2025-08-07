from flask import Flask
from flask_cors import CORS
from app.core.config import Config
from app.core.database import init_db

def create_app():
    app = Flask(__name__)
    
    # Загружаем конфигурацию
    app.config.from_object(Config)
    
    # Настраиваем CORS
    CORS(app)
    
    # Инициализируем базу данных
    init_db(app)
    
    # Регистрируем blueprints
    from app.routes.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app 