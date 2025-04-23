from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from constants import COUNTRY_URLS

# Словарь с URL для разных стран

def parse_winline_data(country='england'):
    # Настройка опций Chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Запуск в фоновом режиме
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Инициализация драйвера
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    url = COUNTRY_URLS[country]['winline']
    matches = []  # Инициализируем список матчей
    
    try:
        # Загрузка страницы
        driver.get(url)
        
        # Ждем загрузку страницы
        time.sleep(5)
        
        # Получаем HTML страницы
        html_content = driver.page_source
        
        # Сохраняем HTML в файл
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        output_file = os.path.join(output_dir, "winline_page.html")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        print(f"\nHTML сохранен в файл: {output_file}")
        
        # Извлекаем данные о матчах
        matches = []
        
        # Ждем появления элементов с матчами
        wait = WebDriverWait(driver, 10)
        match_cards = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, '.card.ng-star-inserted')
        ))
        
        for card in match_cards:
            try:
                # Извлекаем команды
                team_names = card.find_elements(By.CSS_SELECTOR, '.body-left__names .name')
                if len(team_names) >= 2:
                    home_team = team_names[0].text.strip()
                    away_team = team_names[1].text.strip()
                else:
                    continue
                
                # Извлекаем дату и время
                date_time_elem = card.find_element(By.CSS_SELECTOR, '.header-left__time')
                date_time = date_time_elem.text.strip()
                
                # Извлекаем коэффициенты на исход матча
                odds_buttons = card.find_elements(By.CSS_SELECTOR, '.card__market:first-child .coefficient-button span')
                if len(odds_buttons) >= 3:
                    home_odds = odds_buttons[0].text.strip()
                    draw_odds = odds_buttons[1].text.strip()
                    away_odds = odds_buttons[2].text.strip()
                else:
                    continue
                
                match_data = {
                    'date_time': date_time,
                    'home_team': home_team,
                    'away_team': away_team,
                    'home_odds': home_odds,
                    'draw_odds': draw_odds,
                    'away_odds': away_odds
                }
                
                matches.append(match_data)
                
            except Exception as e:
                print(f"Ошибка при извлечении данных матча: {str(e)}")
                continue
        
        # Выводим данные в консоль
        print("\nДанные о матчах:")
        for match in matches:
            print(f"\nМатч: {match['home_team']} - {match['away_team']}")
            print(f"Дата и время: {match['date_time']}")
            print(f"Коэффициенты: Победа хозяев: {match['home_odds']}, Ничья: {match['draw_odds']}, Победа гостей: {match['away_odds']}")
        
        # Сохраняем данные в JSON файл
        json_file = os.path.join(output_dir, f"winline_matches_{country}.json")
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(matches, f, ensure_ascii=False, indent=2)
            
        print(f"\nДанные сохранены в файл: {json_file}")
        
    except Exception as e:
        print(f"Ошибка при парсинге страницы: {str(e)}")
        
    finally:
        driver.quit()
    
    return matches  # Возвращаем список матчей
        