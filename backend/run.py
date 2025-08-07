#!/usr/bin/env python3
"""
Файл для запуска Flask приложения
Экспортирует переменную app для gunicorn
"""

from app import create_app
import os

# Создаем экземпляр приложения
app = create_app()

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=False
    ) 