import requests
from bs4 import BeautifulSoup
import json
import os
from utils import translate_team_name
from datetime import datetime
import time
import re
from team_translations import TEAM_TRANSLATIONS
from constants import COUNTRY_URLS
# Словарь с URL для разных стран

def parse_kickform_data(country_code):
    """
    Парсит данные с thepunterspage.com для указанной страны
    """
    url = COUNTRY_URLS.get(country_code)['kickform']
    print(url)
    if not url:
        raise ValueError(f"Неизвестный код страны: {country_code}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'lxml')
        match_cards = soup.select('.card_new')
        
        matches = []
        
        for card in match_cards:
            try:
                # Извлекаем дату и время
                date_elem = card.select_one('.matchstart_tag')
                time_elem = card.select_one('.matchstart_uhrzeit')
                
                date = date_elem.text.strip() if date_elem else "Нет данных"
                time = time_elem.text.strip() if time_elem else "Нет данных"
                
                # Извлекаем команды
                home_team_elem = card.select_one('.team.home .teamname')
                away_team_elem = card.select_one('.team.away .teamname')
                
                home_team = home_team_elem.text.strip() if home_team_elem else "Нет данных"
                away_team = away_team_elem.text.strip() if away_team_elem else "Нет данных"
                
                # Переводим названия команд на русский язык
                home_team_ru = translate_team_name(home_team)
                away_team_ru = translate_team_name(away_team)
                
                # Извлекаем прогнозы
                home_percent_elem = card.select_one('.predict .first .prozent')
                draw_percent_elem = card.select_one('.predict .second .prozent')
                away_percent_elem = card.select_one('.predict .third .prozent')
                
                home_percent = int(re.sub(r'[^\d]', '', home_percent_elem.text)) if home_percent_elem else 0
                draw_percent = int(re.sub(r'[^\d]', '', draw_percent_elem.text)) if draw_percent_elem else 0
                away_percent = int(re.sub(r'[^\d]', '', away_percent_elem.text)) if away_percent_elem else 0
                
                # Извлекаем рекомендуемый счет
                score_elem = card.select_one('.tipp-box strong')
                recommended_score = score_elem.text.strip() if score_elem else "Нет данных"
                
                match_data = {
                    "date": date,
                    "time": time,
                    "home": home_team_ru,  # Используем русское название
                    "away": away_team_ru,  # Используем русское название
                    "home_percent": home_percent,
                    "draw_percent": draw_percent,
                    "away_percent": away_percent,
                    "recommended_score": recommended_score,
                    "source": "thepunterspage",
                    "home_odds": None,  # Будет заполнено позже
                    "draw_odds": None,  # Будет заполнено позже
                    "away_odds": None   # Будет заполнено позже
                }
                
                matches.append(match_data)
                
            except Exception as e:
                print(f"Ошибка при парсинге карточки матча: {e}")
                continue
        
        return matches
    
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return [] 

def save_kickform_data(matches, country_code):
    """
    Сохраняет данные в JSON файл
    """
    # Создаем директорию, если она не существует
    os.makedirs('kickform_data', exist_ok=True)
    
    # Формируем имя файла
    filename = f'kickform_data/kickform_matches_{country_code}.json'
    
    # Сохраняем данные
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({
            'country': country_code,
            'last_updated': datetime.now().isoformat(),
            'matches': matches
        }, f, ensure_ascii=False, indent=2)
    
    print(f"Данные для {country_code} сохранены в {filename}")

def parse_all_countries():
    """
    Парсит данные для всех стран
    """
    for country_code in COUNTRY_URLS.keys():
        print(f"Парсинг данных для {country_code}...")
        matches = parse_kickform_data(country_code)
        if matches:
            save_kickform_data(matches, country_code)
        # Добавляем задержку между запросами
        time.sleep(2)

if __name__ == '__main__':
    parse_all_countries() 