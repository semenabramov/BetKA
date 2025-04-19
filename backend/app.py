from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from kickform_parser import parse_kickform_data, save_kickform_data
from utils import (
    load_winline_data, 
    find_matching_match_by_teams,
    prepare_data_for_prediction,
    process_predictions
)
from winline_parser import parse_winline_data
import os
import json
import glob

app = Flask(__name__)
CORS(app)

def load_all_kickform_data():
    """
    Загружает данные о матчах из всех JSON-файлов в папке kickform_data
    """
    all_matches = []
    
    # Получаем список всех JSON-файлов в папке kickform_data
    kickform_files = glob.glob('kickform_data/kickform_matches_*.json')
    
    for file_path in kickform_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Добавляем матчи из текущего файла в общий список
                all_matches.extend(data['matches'])
        except Exception as e:
            print(f"Ошибка при загрузке файла {file_path}: {str(e)}")
    
    return all_matches

def load_all_winline_data():
    """
    Загружает данные о матчах из всех JSON-файлов в папке output
    """
    all_matches = []
    
    # Получаем список всех JSON-файлов в папке output
    winline_files = glob.glob('output/winline_matches_*.json')
    
    for file_path in winline_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Проверяем формат данных
                if isinstance(data, dict) and 'matches' in data:
                    # Формат: {"matches": [...]}
                    matches = data['matches']
                elif isinstance(data, list):
                    # Формат: [...]
                    matches = data
                else:
                    print(f"Неизвестный формат данных в файле {file_path}")
                    continue
                
                # Добавляем матчи из текущего файла в общий список
                all_matches.extend(matches)
        except Exception as e:
            print(f"Ошибка при загрузке файла {file_path}: {str(e)}")
    
    return all_matches

@app.route('/api/matches', methods=['GET'])
def get_matches():
    country = request.args.get('country', 'all')
    
    # Загружаем все данные о матчах из kickform_data
    matches_punterspage = load_all_kickform_data()
    
    # Фильтруем по стране, если указана конкретная страна
    if country != 'all':
        matches_punterspage = [match for match in matches_punterspage if match.get('country') == country]
    
    # Загружаем все данные с Winline
    matches_winline = load_all_winline_data()
    
    # Объединяем данные
    for match in matches_punterspage:
        matching_winline_match = find_matching_match_by_teams(match, matches_winline)
        if matching_winline_match:
            # Добавляем коэффициенты из Winline
            match["home_odds"] = matching_winline_match.get("home_odds", "")
            match["draw_odds"] = matching_winline_match.get("draw_odds", "")
            match["away_odds"] = matching_winline_match.get("away_odds", "")
    
    # Обрабатываем данные с помощью функции predict_bets
    predictions = process_predictions(matches_punterspage)
    
    # Добавляем предсказания к ответу
    response = {
        "matches": matches_punterspage,
        "predictions": predictions
    }
    
    return jsonify(response)

@app.route('/api/update-kickform', methods=['POST'])
def update_kickform():
    try:
        data = request.get_json()
        country = data.get('country', 'england')
        
        # Парсим новые данные
        matches = parse_kickform_data(country)
        if matches:
            save_kickform_data(matches, country)
            return jsonify({"status": "success", "message": "Данные Kickform успешно обновлены"})
        else:
            return jsonify({"status": "error", "message": "Не удалось получить данные"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

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