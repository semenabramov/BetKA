from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from parser import parse_match_data
from utils import (
    load_winline_data, 
    find_matching_match_by_teams,
    prepare_data_for_prediction,
    process_predictions
)
from winline_parser import parse_winline_data

app = Flask(__name__)
CORS(app)

@app.route('/api/matches', methods=['GET'])
def get_matches():
    country = request.args.get('country', 'england')
    initial_bankroll = int(request.args.get('initial_bankroll', 10000))
    fraction = int(request.args.get('fraction', 3))
    min_bankroll = int(request.args.get('min_bankroll', 100))
    
    # Получаем данные с thepunterspage
    matches_punterspage = parse_match_data(country)
    
    # Загружаем данные с Winline из JSON-файла
    matches_winline = load_winline_data(country)
    
    # Объединяем данные
    for punterspage_match in matches_punterspage:
        matching_winline_match = find_matching_match_by_teams(punterspage_match, matches_winline)
        
        if matching_winline_match:
            # Добавляем коэффициенты из Winline
            punterspage_match["home_odds"] = matching_winline_match["home_odds"]
            punterspage_match["draw_odds"] = matching_winline_match["draw_odds"]
            punterspage_match["away_odds"] = matching_winline_match["away_odds"]
    
    # Обрабатываем данные с помощью функции predict_bets
    predictions = process_predictions(matches_punterspage, initial_bankroll, fraction, min_bankroll)
    
    # Добавляем предсказания к ответу
    response = {
        "matches": matches_punterspage,
        "predictions": predictions
    }
    
    return jsonify(response)

@app.route('/api/update-winline', methods=['POST'])
def update_winline():
    try:
        data = request.get_json()
        country = data.get('country', 'england')
        
        # Запускаем парсер Winline для обновления данных
        parse_winline_data(country)
        return jsonify({"status": "success", "message": "Данные Winline успешно обновлены"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 