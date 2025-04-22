from flask_sqlalchemy import SQLAlchemy
import pymysql

# Заменяем MySQLdb на PyMySQL
pymysql.install_as_MySQLdb()

db = SQLAlchemy()

def init_db(app):
    """Инициализация подключения к базе данных"""
    db.init_app(app)
    
    with app.app_context():
        try:
            # Проверяем подключение к базе данных
            db.engine.connect()
            print('MySQL Connected...')
        except Exception as e:
            print(f'Error connecting to MySQL: {str(e)}')
            raise e 