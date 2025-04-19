import json
import os
import pandas as pd
from prognoz import predict_bets
from team_translations import TEAM_TRANSLATIONS


def translate_team_name(team_name):
    """
    Переводит название команды на русский язык (транслитом)
    """
    # Проверяем, есть ли точное совпадение в словаре
    if team_name in TEAM_TRANSLATIONS:
        return TEAM_TRANSLATIONS[team_name]
    
    # Если точного совпадения нет, пытаемся найти частичное совпадение
    for eng_name, rus_name in TEAM_TRANSLATIONS.items():
        if eng_name.lower() in team_name.lower() or team_name.lower() in eng_name.lower():
            return rus_name
    
    # Если совпадений нет, возвращаем оригинальное название
    return team_name

def load_winline_data(country='england'):
    """
    Загружает данные о матчах из JSON-файла
    """
    try:
        json_file = os.path.join("output", f"winline_matches_{country}.json")
        if os.path.exists(json_file):
            with open(json_file, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            print(f"Файл {json_file} не найден")
            return []
    except Exception as e:
        print(f"Ошибка при загрузке данных из JSON: {e}")
        return []

def find_matching_match_by_teams(match, matches_winline):
    """
    Находит соответствующий матч в данных Winline по названиям команд
    """
    home_team = match.get('home', '')
    away_team = match.get('away', '')
    
    for winline_match in matches_winline:
        # Проверяем разные форматы данных
        winline_home = winline_match.get('home_team', '').lower()
        winline_away = winline_match.get('away_team', '').lower()
        
        # Проверяем совпадение команд (без учета регистра)
        if (home_team.lower() == winline_home.lower() and 
            away_team.lower() == winline_away.lower()):
            return winline_match
    
    return None

def prepare_data_for_prediction(matches):
    """
    Подготавливает данные для функции predict_bets
    """
    prediction_data = []
    
    for match in matches:
        # Проверяем, что у нас есть все необходимые данные
        if match["home_odds"] and match["draw_odds"] and match["away_odds"]:
            # Преобразуем проценты в десятичные дроби
            home_confidence = match["home_percent"] / 100
            draw_confidence = match["draw_percent"] / 100
            away_confidence = match["away_percent"] / 100
            
            # Преобразуем строковые коэффициенты в числа
            try:
                home_odds = float(match["home_odds"])
                draw_odds = float(match["draw_odds"])
                away_odds = float(match["away_odds"])
                
                prediction_data.append({
                    "home": match["home"],
                    "away": match["away"],
                    "odds_home": home_odds,
                    "odds_draw": draw_odds,
                    "odds_away": away_odds,
                    "confidence_home": home_confidence,
                    "confidence_draw": draw_confidence,
                    "confidence_away": away_confidence
                })
            except (ValueError, TypeError):
                print(f"Ошибка при преобразовании коэффициентов для матча {match['home']} - {match['away']}")
                continue
    
    return prediction_data

def process_predictions(matches,initial_bankroll=10000, fraction=3, min_bankroll=100):
    """
    Обрабатывает данные с помощью функции predict_bets
    """
    # Подготавливаем данные для предсказания
    prediction_data = prepare_data_for_prediction(matches)
    
    if not prediction_data:
        return []
    
    # Преобразуем данные в DataFrame
    df = pd.DataFrame(prediction_data,)
    
    # Вызываем функцию predict_bets
    try:
        results = predict_bets(df, initial_bankroll, fraction, min_bankroll)
        
        # Преобразуем результаты в список словарей
        if not results.empty:
            return results.to_dict('records')
        else:
            return []
    except Exception as e:
        print(f"Ошибка при обработке предсказаний: {e}")
        return [] 