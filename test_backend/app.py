from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return jsonify({
        'message': 'Сервер запущен!',
        'status': 'success',
        'service': 'BetKA Test Backend'
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'Сервер работает нормально'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 