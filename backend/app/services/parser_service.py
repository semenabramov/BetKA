import requests
from bs4 import BeautifulSoup
import json
import logging
from datetime import datetime
from app.core.database import db
from app.models.odds_source import OddsSource
from app.models.match import Match
from app.models.team import Team
from app.models.odds import OddsFromSource
from app.models.bookmaker import Bookmaker
from app.models.odds import BookmakerOdds
from app.models.alias_team import AliasTeam
from sqlalchemy import or_
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

logger = logging.getLogger(__name__)

class ParserService:
    @staticmethod
    def parse_matches_from_source(source_id=None):
        """
        Парсит матчи с указанного источника или всех активных источников
        
        Args:
            source_id (int, optional): ID источника для парсинга. Если None, парсит все активные источники.
            
        Returns:
            dict: Результат парсинга с информацией о количестве обработанных матчей и списком матчей
        """
        try:
            # Получаем активные источники
            if source_id:
                sources = OddsSource.query.filter_by(id=source_id, is_active=True).all()
            else:
                sources = OddsSource.query.filter_by(is_active=True).all()
                
            if not sources:
                return {
                    'status': 'error',
                    'message': 'Нет активных источников для парсинга',
                    'matches': []
                }
                
            total_matches = 0
            results = []
            
            for source in sources:
                logger.info(f"Начинаем парсинг с источника: {source.name}")
                
                # Собираем все URL лиг
                league_urls = [
                    source.premier_league_url,
                    source.championship_url,
                    source.league_one_url,
                    source.league_two_url,
                    source.bundesliga_one_url,
                    source.bundesliga_two_url,
                    source.liga_url,
                    source.la_liga_url,
                    source.serie_a_url,
                    source.ligue_one_url
                ]
                
                # Фильтруем None значения
                league_urls = [url for url in league_urls if url]
                
                if not league_urls:
                    logger.warning(f"У источника {source.name} нет URL лиг для парсинга")
                    continue
                
                # Парсим каждую лигу
                for url in league_urls:
                    logger.info(f"Парсим матчи с {url}")
                    try:
                        matches = ParserService._parse_league(url, source)
                        # Добавляем ID источника к каждому матчу
                        for match in matches:
                            match['source_id'] = source.id
                        total_matches += len(matches)
                        results.extend(matches)
                        logger.info(f"Успешно спарсили {len(matches)} матчей с {url}")
                    except Exception as e:
                        logger.error(f"Ошибка при парсинге {url}: {str(e)}")
            
            logger.info(f"Всего спарсировано {total_matches} матчей с источников")
            
            return {
                'status': 'success',
                'message': f'Успешно спарсировано {total_matches} матчей',
                'matches': results,
                'matches_count': total_matches
            }
            
        except Exception as e:
            logger.error(f"Ошибка при парсинге матчей: {str(e)}")
            return {
                'status': 'error',
                'message': f'Ошибка при парсинге матчей: {str(e)}',
                'matches': []
            }
    
    @staticmethod
    def parse_bookmaker_matches(bookmaker_id=None):
        """
        Парсит матчи с указанного букмекера или всех букмекеров
        
        Args:
            bookmaker_id (int, optional): ID букмекера для парсинга. Если None, парсит все букмекеры.
            
        Returns:
            dict: Результат парсинга с информацией о количестве обработанных матчей и списком матчей
        """
        try:
            # Получаем букмекеров
            if bookmaker_id:
                bookmakers = Bookmaker.query.filter_by(id=bookmaker_id).all()
            else:
                bookmakers = Bookmaker.query.all()
                
            if not bookmakers:
                return {
                    'status': 'error',
                    'message': 'Нет букмекеров для парсинга',
                    'matches': []
                }
                
            total_matches = 0
            results = []
            
            for bookmaker in bookmakers:
                logger.info(f"Начинаем парсинг с букмекера: {bookmaker.name}")
                
                # Собираем все URL лиг
                league_urls = [
                    bookmaker.premier_league_url,
                    bookmaker.championship_url,
                    bookmaker.league_one_url,
                    bookmaker.league_two_url,
                    bookmaker.bundesliga_one_url,
                    bookmaker.bundesliga_two_url,
                    bookmaker.liga_url,
                    bookmaker.la_liga_url,
                    bookmaker.serie_a_url,
                    bookmaker.ligue_one_url
                ]
                
                # Фильтруем None значения
                league_urls = [url for url in league_urls if url]
                
                if not league_urls:
                    logger.warning(f"У букмекера {bookmaker.name} нет URL лиг для парсинга")
                    continue
                
                # Парсим каждую лигу
                for url in league_urls:
                    logger.info(f"Парсим матчи с {url}")
                    try:
                        matches = ParserService._parse_bookmaker_league(url, bookmaker)
                        # Добавляем ID букмекера к каждому матчу
                        for match in matches:
                            match['bookmaker_id'] = bookmaker.id
                        total_matches += len(matches)
                        results.extend(matches)
                        logger.info(f"Успешно спарсили {len(matches)} матчей с {url}")
                    except Exception as e:
                        logger.error(f"Ошибка при парсинге {url}: {str(e)}")
            
            logger.info(f"Всего спарсировано {total_matches} матчей с букмекеров")
            
            return {
                'status': 'success',
                'message': f'Успешно спарсировано {total_matches} матчей с букмекеров',
                'matches': results,
                'matches_count': total_matches
            }
            
        except Exception as e:
            logger.error(f"Ошибка при парсинге матчей с букмекеров: {str(e)}")
            return {
                'status': 'error',
                'message': f'Ошибка при парсинге матчей с букмекеров: {str(e)}',
                'matches': []
            }
    
    @staticmethod
    def _parse_league(url, source):
        """
        Парсит матчи с указанной лиги
        
        Args:
            url (str): URL лиги
            source (OddsSource): Объект источника
            
        Returns:
            list: Список спарсенных матчей
        """
        matches = []
        
        try:
            # Получаем HTML страницы
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Парсим HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Находим все карточки матчей
            match_cards = soup.select('.card_new')
            
            for card in match_cards:
                try:
                    # Извлекаем названия команд
                    home_team_name = card.select_one('.team.home .teamname').text.strip()
                    away_team_name = card.select_one('.team.away .teamname').text.strip()
                    
                    # Ищем команды в базе данных
                    home_team = Team.query.filter(
                        or_(
                            Team.name == home_team_name,
                            Team.aliases.any(AliasTeam.alias_name == home_team_name)
                        )
                    ).first()
                    
                    away_team = Team.query.filter(
                        or_(
                            Team.name == away_team_name,
                            Team.aliases.any(AliasTeam.alias_name == away_team_name)
                        )
                    ).first()
                    
                    if not home_team or not away_team:
                        logger.warning(f"Не найдены команды: {home_team_name} или {away_team_name}")
                        continue
                    
                    # Находим активную вкладку с коэффициентами
                    active_tab = card.select_one('.tab-pane.active')
                    if not active_tab:
                        logger.warning(f"Не найдена активная вкладка для матча {home_team_name} vs {away_team_name}")
                        continue
                        
                    # Извлекаем коэффициенты из активной вкладки
                    predict = active_tab.select_one('.predict')
                    if not predict:
                        logger.warning(f"Не найдены коэффициенты для матча {home_team_name} vs {away_team_name}")
                        continue
                        
                    odds_elements = predict.select('.prozent')
                    if len(odds_elements) != 3:
                        logger.warning(f"Неверное количество коэффициентов для матча {home_team_name} vs {away_team_name}")
                        continue
                    
                    # Удаляем тег <small>%</small> и преобразуем в float
                    odds_home = float(odds_elements[0].get_text(strip=True).replace('%', ''))
                    odds_draw = float(odds_elements[1].get_text(strip=True).replace('%', ''))
                    odds_away = float(odds_elements[2].get_text(strip=True).replace('%', ''))
                    
                    # Извлекаем дату и время
                    date_str = card.select_one('.matchstart_tag').text.strip()
                    time_str = card.select_one('.matchstart_uhrzeit').text.strip()
                    
                    # Преобразуем дату и время в datetime
                    match_date = datetime.strptime(f"{date_str} {time_str}", '%d.%m.%Y %H:%M')
                    
                    # Создаем объект матча с ID команд
                    match_data = {
                        'date': match_date.isoformat(),
                        'team_home': home_team.id,
                        'team_away': away_team.id,
                        'odds': {
                            'home': odds_home,
                            'draw': odds_draw,
                            'away': odds_away
                        }
                    }
                    
                    matches.append(match_data)
                except Exception as e:
                    logger.error(f"Ошибка при парсинге матча: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Ошибка при запросе {url}: {str(e)}")
            
        return matches
    
    @staticmethod
    def _parse_bookmaker_league(url, bookmaker):
        """
        Парсит матчи с указанной лиги букмекера с использованием Selenium
        
        Args:
            url (str): URL лиги
            bookmaker (Bookmaker): Объект букмекера
            
        Returns:
            list: Список спарсенных матчей
        """
        matches = []
        
        try:
            # Настройка Chrome в безголовом режиме
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            # Инициализация драйвера
            driver = webdriver.Chrome(options=chrome_options)
            
            try:
                # Загрузка страницы
                logger.info(f"Загрузка страницы {url}")
                driver.get(url)
                
                # Ожидание загрузки контента
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".card.ng-star-inserted, .event-item, .match-item, .game-item"))
                )
                
                # Даем время для полной загрузки динамического контента
                time.sleep(5)
                
                # Получаем HTML после выполнения JavaScript
                page_source = driver.page_source
                
                # Сохраняем HTML в файл для отладки
                # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                # debug_filename = f"debug_{bookmaker.name}_{timestamp}.html"
                # with open(debug_filename, "w", encoding="utf-8") as f:
                #     f.write(page_source)
                # logger.info(f"HTML сохранен в файл: {debug_filename}")
                
                # Парсим HTML с помощью BeautifulSoup
                soup = BeautifulSoup(page_source, 'html.parser')
                
                # Находим все карточки матчей (пробуем разные селекторы)
                match_cards = soup.select(".card.ng-star-inserted, .event-item, .match-item, .game-item")
                
                if not match_cards:
                    logger.warning(f"Не найдены карточки матчей на странице {url}")
                    return matches
                
                logger.info(f"Найдено {len(match_cards)} матчей на странице {url}")
                
                for card in match_cards:
                    try:
                        # Извлекаем названия команд (пробуем разные селекторы)
                        team_names = card.select(".body-left__names .name, .team-home .team-name, .home-team .name, .team1 .name")
                        if len(team_names) >= 2:
                            home_team_name = team_names[0].text.strip()
                            away_team_name = team_names[1].text.strip()
                        else:
                            # Пробуем альтернативные селекторы
                            home_team_element = card.select_one(".team-home .team-name, .home-team .name, .team1 .name")
                            away_team_element = card.select_one(".team-away .team-name, .away-team .name, .team2 .name")
                            
                            if not home_team_element or not away_team_element:
                                continue
                                
                            home_team_name = home_team_element.text.strip()
                            away_team_name = away_team_element.text.strip()
                        
                        # Ищем команды в базе данных
                        home_team = Team.query.filter(
                            or_(
                                Team.name == home_team_name,
                                Team.aliases.any(AliasTeam.alias_name == home_team_name)
                            )
                        ).first()
                        
                        away_team = Team.query.filter(
                            or_(
                                Team.name == away_team_name,
                                Team.aliases.any(AliasTeam.alias_name == away_team_name)
                            )
                        ).first()
                        
                        if not home_team or not away_team:
                            logger.warning(f"Не найдены команды: {home_team_name} или {away_team_name}")
                            continue
                        
                        # Извлекаем коэффициенты (пробуем разные селекторы)
                        odds_buttons = card.select(".card__market:first-child .coefficient-button span, .odds-container .odd-home, .odds-container .odd-draw, .odds-container .odd-away")
                        
                        if len(odds_buttons) >= 3:
                            odds_home = float(odds_buttons[0].text.strip())
                            odds_draw = float(odds_buttons[1].text.strip())
                            odds_away = float(odds_buttons[2].text.strip())
                        else:
                            # Пробуем альтернативные селекторы
                            odds_container = card.select_one(".odds-container, .coefficients, .odds")
                            if not odds_container:
                                continue
                                
                            odds_home_element = odds_container.select_one(".odd-home, .coefficient-home, .home-odd")
                            odds_draw_element = odds_container.select_one(".odd-draw, .coefficient-draw, .draw-odd")
                            odds_away_element = odds_container.select_one(".odd-away, .coefficient-away, .away-odd")
                            
                            if not odds_home_element or not odds_draw_element or not odds_away_element:
                                continue
                                
                            odds_home = float(odds_home_element.text.strip())
                            odds_draw = float(odds_draw_element.text.strip())
                            odds_away = float(odds_away_element.text.strip())
                        
                        # Извлекаем дату и время (пробуем разные селекторы)
                        date_time_elem = card.select_one(".header-left__time, .event-date, .match-date, .date")
                        if date_time_elem:
                            date_time = date_time_elem.text.strip()
                            # Пытаемся разделить дату и время
                            try:
                                date_str, time_str = date_time.split(" ", 1)
                            except ValueError:
                                # Если не удалось разделить, пробуем другие селекторы
                                date_element = card.select_one(".event-date, .match-date, .date")
                                time_element = card.select_one(".event-time, .match-time, .time")
                                
                                if not date_element or not time_element:
                                    continue
                                    
                                date_str = date_element.text.strip()
                                time_str = time_element.text.strip()
                        else:
                            # Пробуем альтернативные селекторы
                            date_element = card.select_one(".event-date, .match-date, .date")
                            time_element = card.select_one(".event-time, .match-time, .time")
                            
                            if not date_element or not time_element:
                                continue
                                
                            date_str = date_element.text.strip()
                            time_str = time_element.text.strip()
                        
                        # Преобразуем дату и время в datetime
                        try:
                            match_date = datetime.strptime(f"{date_str} {time_str}", '%d.%m.%Y %H:%M')
                        except ValueError:
                            # Пробуем другие форматы даты
                            try:
                                match_date = datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M')
                            except ValueError:
                                try:
                                    match_date = datetime.strptime(f"{date_str} {time_str}", '%d.%m.%y %H:%M')
                                except ValueError:
                                    logger.warning(f"Не удалось распарсить дату: {date_str} {time_str}")
                                    continue
                        
                        # Создаем объект матча
                        match_data = {
                            'date': match_date.isoformat(),
                            'team_home': home_team.id,
                            'team_away': away_team.id,
                            'odds': {
                                'home': odds_home,
                                'draw': odds_draw,
                                'away': odds_away
                            }
                        }
                        
                        matches.append(match_data)
                        logger.info(f"Успешно спарсирован матч: {home_team_name} vs {away_team_name}")
                    except Exception as e:
                        logger.error(f"Ошибка при парсинге матча: {str(e)}")
                        continue
            finally:
                # Закрываем драйвер
                driver.quit()
                    
        except Exception as e:
            logger.error(f"Ошибка при парсинге {url}: {str(e)}")
            
        return matches
    
    @staticmethod
    def save_parsed_matches(matches_data, source_id):
        """
        Сохраняет спарсенные матчи в базу данных
        
        Args:
            matches_data (list): Список матчей для сохранения
            source_id (int): ID источника
            
        Returns:
            dict: Результат сохранения
        """
        try:
            saved_matches = 0
            updated_odds = 0
            
            for match_data in matches_data:
                # Ищем матч по дате и ID команд
                match = Match.query.filter_by(
                    date=datetime.fromisoformat(match_data['date']),
                    team_home=match_data['team_home'],
                    team_away=match_data['team_away']
                ).first()
                
                if not match:
                    # Создаем новый матч
                    match = Match(
                        date=datetime.fromisoformat(match_data['date']),
                        team_home=match_data['team_home'],
                        team_away=match_data['team_away']
                    )
                    db.session.add(match)
                    db.session.flush()  # Получаем ID матча
                    saved_matches += 1
                
                # Проверяем, есть ли уже коэффициенты от этого источника
                odds = OddsFromSource.query.filter_by(
                    match_id=match.id,
                    sources_id=source_id
                ).first()
                
                if odds:
                    # Обновляем существующие коэффициенты
                    odds.odds_home = match_data['odds']['home']
                    odds.odds_draw = match_data['odds']['draw']
                    odds.odds_away = match_data['odds']['away']
                    updated_odds += 1
                else:
                    # Создаем новые коэффициенты
                    odds = OddsFromSource(
                        match_id=match.id,
                        sources_id=source_id,
                        odds_home=match_data['odds']['home'],
                        odds_draw=match_data['odds']['draw'],
                        odds_away=match_data['odds']['away']
                    )
                    db.session.add(odds)
            
            db.session.commit()
            
            return {
                'status': 'success',
                'message': f'Сохранено {saved_matches} новых матчей, обновлено {updated_odds} коэффициентов'
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Ошибка при сохранении матчей: {str(e)}")
            return {
                'status': 'error',
                'message': f'Ошибка при сохранении матчей: {str(e)}'
            }
    
    @staticmethod
    def save_bookmaker_matches(matches_data, bookmaker_id):
        """
        Сохраняет спарсенные матчи букмекеров в базу данных
        
        Args:
            matches_data (list): Список матчей для сохранения
            bookmaker_id (int): ID букмекера
            
        Returns:
            dict: Результат сохранения
        """
        try:
            saved_matches = 0
            updated_odds = 0
            
            for match_data in matches_data:
                # Ищем соответствующий матч в базе данных
                match = Match.query.filter_by(
                    date=datetime.fromisoformat(match_data['date']),
                    team_home=match_data['team_home'],
                    team_away=match_data['team_away']
                ).first()
                
                if not match:
                    # Создаем новый матч
                    match = Match(
                        date=datetime.fromisoformat(match_data['date']),
                        team_home=match_data['team_home'],
                        team_away=match_data['team_away']
                    )
                    db.session.add(match)
                    db.session.flush()  # Получаем ID матча
                    saved_matches += 1
                
                # Проверяем, есть ли уже коэффициенты от этого букмекера
                odds = BookmakerOdds.query.filter_by(
                    match_id=match.id,
                    bookmaker_id=bookmaker_id
                ).first()
                
                if odds:
                    # Обновляем существующие коэффициенты
                    odds.odds_home = match_data['odds']['home']
                    odds.odds_draw = match_data['odds']['draw']
                    odds.odds_away = match_data['odds']['away']
                    updated_odds += 1
                else:
                    # Создаем новые коэффициенты
                    odds = BookmakerOdds(
                        match_id=match.id,
                        bookmaker_id=bookmaker_id,
                        odds_home=match_data['odds']['home'],
                        odds_draw=match_data['odds']['draw'],
                        odds_away=match_data['odds']['away']
                    )
                    db.session.add(odds)
            
            db.session.commit()
            
            return {
                'status': 'success',
                'message': f'Сохранено {saved_matches} новых матчей, обновлено {updated_odds} коэффициентов'
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Ошибка при сохранении матчей: {str(e)}")
            return {
                'status': 'error',
                'message': f'Ошибка при сохранении матчей: {str(e)}'
            }
    
    @staticmethod
    def compare_and_merge_matches(source_matches, bookmaker_matches):
        """
        Сравнивает и объединяет матчи из разных источников
        
        Args:
            source_matches (list): Список матчей из источников
            bookmaker_matches (list): Список матчей из букмекеров
            
        Returns:
            dict: Результат объединения с информацией о количестве объединенных матчей
        """
        try:
            logger.info(f"Загружено {len(source_matches)} матчей из источников и {len(bookmaker_matches)} матчей из букмекеров")
            
            # Создаем словарь для объединенных матчей
            merged_matches = {}
            
            # Обрабатываем матчи из источников
            for match in source_matches:
                # Создаем уникальный ключ для матча (только ID команд, без даты)
                match_key = f"{match['team_home']}_{match['team_away']}"
                
                # Извлекаем только дату (год, месяц, день) без времени
                match_date = datetime.fromisoformat(match['date']).date()
                
                if match_key not in merged_matches:
                    merged_matches[match_key] = {
                        'date': match['date'],
                        'team_home': match['team_home'],
                        'team_away': match['team_away'],
                        'source_odds': [],
                        'bookmaker_odds': []
                    }
                else:
                    # Если матч уже существует, обновляем дату, если она более поздняя
                    # (предполагаем, что более поздняя дата более актуальна)
                    existing_date = datetime.fromisoformat(merged_matches[match_key]['date']).date()
                    if match_date > existing_date:
                        merged_matches[match_key]['date'] = match['date']
                
                # Добавляем коэффициенты из источника
                if 'odds' in match:
                    source_id = match.get('source_id', 0)
                    merged_matches[match_key]['source_odds'].append({
                        'source_id': source_id,
                        'odds_home': match['odds']['home'],
                        'odds_draw': match['odds']['draw'],
                        'odds_away': match['odds']['away']
                    })
            
            # Обрабатываем матчи из букмекеров
            for match in bookmaker_matches:
                # Создаем уникальный ключ для матча (только ID команд, без даты)
                match_key = f"{match['team_home']}_{match['team_away']}"
                
                # Извлекаем только дату (год, месяц, день) без времени
                match_date = datetime.fromisoformat(match['date']).date()
                
                if match_key not in merged_matches:
                    merged_matches[match_key] = {
                        'date': match['date'],
                        'team_home': match['team_home'],
                        'team_away': match['team_away'],
                        'source_odds': [],
                        'bookmaker_odds': []
                    }
                else:
                    # Если матч уже существует, обновляем дату, если она более поздняя
                    existing_date = datetime.fromisoformat(merged_matches[match_key]['date']).date()
                    if match_date > existing_date:
                        merged_matches[match_key]['date'] = match['date']
                
                # Добавляем коэффициенты из букмекера
                if 'odds' in match:
                    bookmaker_id = match.get('bookmaker_id', 0)
                    merged_matches[match_key]['bookmaker_odds'].append({
                        'bookmaker_id': bookmaker_id,
                        'odds_home': match['odds']['home'],
                        'odds_draw': match['odds']['draw'],
                        'odds_away': match['odds']['away']
                    })
            
            # Фильтруем матчи, оставляя только те, которые есть и в источниках, и у букмекеров
            filtered_matches = {
                key: match for key, match in merged_matches.items()
                if match['source_odds'] and match['bookmaker_odds']
            }
            
            logger.info(f"После фильтрации осталось {len(filtered_matches)} матчей, которые есть и в источниках, и у букмекеров")
            
            # Сохраняем объединенные матчи в JSON файл
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            merged_file = f"merged_matches_{timestamp}.json"
            
            with open(merged_file, 'w', encoding='utf-8') as f:
                json.dump(list(filtered_matches.values()), f, ensure_ascii=False, indent=2)
                
            logger.info(f"Объединенные матчи сохранены в файл {merged_file}")
            
            # Сохраняем объединенные матчи в базу данных
            db_result = ParserService.save_merged_matches_to_db(list(filtered_matches.values()))
            
            return {
                'status': 'success',
                'message': f'Успешно объединено {len(filtered_matches)} матчей',
                'merged_matches': len(filtered_matches),
                'merged_file': merged_file,
                'merged_data': list(filtered_matches.values()),
                'db_result': db_result
            }
            
        except Exception as e:
            logger.error(f"Ошибка при объединении матчей: {str(e)}")
            return {
                'status': 'error',
                'message': f'Ошибка при объединении матчей: {str(e)}',
                'merged_data': []
            }
    
    @staticmethod
    def save_merged_matches_to_db(merged_matches):
        """
        Сохраняет объединенные матчи в базу данных
        
        Args:
            merged_matches (list): Список объединенных матчей
            
        Returns:
            dict: Результат сохранения с информацией о количестве сохраненных и обновленных матчей
        """
        try:
            saved_matches = 0
            updated_matches = 0
            saved_source_odds = 0
            saved_bookmaker_odds = 0
            
            for match_data in merged_matches:
                # Проверяем, существует ли матч в базе данных
                match_date = datetime.fromisoformat(match_data['date'])
                team_home = match_data['team_home']
                team_away = match_data['team_away']
                
                # Ищем матч по дате и командам
                match = Match.query.filter_by(
                    date=match_date,
                    team_home=team_home,
                    team_away=team_away
                ).first()
                
                if not match:
                    # Создаем новый матч
                    match = Match(
                        date=match_date,
                        team_home=team_home,
                        team_away=team_away
                    )
                    db.session.add(match)
                    db.session.flush()  # Получаем ID матча
                    saved_matches += 1
                else:
                    updated_matches += 1
                
                # Сохраняем коэффициенты из источников
                for source_odds in match_data.get('source_odds', []):
                    source_id = source_odds.get('source_id')
                    if not source_id:
                        continue
                    
                    # Проверяем, есть ли уже коэффициенты от этого источника
                    odds = OddsFromSource.query.filter_by(
                        match_id=match.id,
                        sources_id=source_id
                    ).first()
                    
                    if odds:
                        # Обновляем существующие коэффициенты
                        odds.odds_home = source_odds['odds_home']
                        odds.odds_draw = source_odds['odds_draw']
                        odds.odds_away = source_odds['odds_away']
                    else:
                        # Создаем новые коэффициенты
                        odds = OddsFromSource(
                            match_id=match.id,
                            sources_id=source_id,
                            odds_home=source_odds['odds_home'],
                            odds_draw=source_odds['odds_draw'],
                            odds_away=source_odds['odds_away']
                        )
                        db.session.add(odds)
                    
                    saved_source_odds += 1
                
                # Сохраняем коэффициенты из букмекеров
                for bookmaker_odds in match_data.get('bookmaker_odds', []):
                    bookmaker_id = bookmaker_odds.get('bookmaker_id')
                    if not bookmaker_id:
                        continue
                    
                    # Проверяем, есть ли уже коэффициенты от этого букмекера
                    odds = BookmakerOdds.query.filter_by(
                        match_id=match.id,
                        bookmaker_id=bookmaker_id
                    ).first()
                    
                    if odds:
                        # Обновляем существующие коэффициенты
                        odds.odds_home = bookmaker_odds['odds_home']
                        odds.odds_draw = bookmaker_odds['odds_draw']
                        odds.odds_away = bookmaker_odds['odds_away']
                    else:
                        # Создаем новые коэффициенты
                        odds = BookmakerOdds(
                            match_id=match.id,
                            bookmaker_id=bookmaker_id,
                            odds_home=bookmaker_odds['odds_home'],
                            odds_draw=bookmaker_odds['odds_draw'],
                            odds_away=bookmaker_odds['odds_away']
                        )
                        db.session.add(odds)
                    
                    saved_bookmaker_odds += 1
            
            # Сохраняем изменения в базе данных
            db.session.commit()
            
            logger.info(f"Сохранено {saved_matches} новых матчей, обновлено {updated_matches} существующих матчей")
            logger.info(f"Сохранено {saved_source_odds} коэффициентов из источников и {saved_bookmaker_odds} коэффициентов из букмекеров")
            
            return {
                'saved_matches': saved_matches,
                'updated_matches': updated_matches,
                'saved_source_odds': saved_source_odds,
                'saved_bookmaker_odds': saved_bookmaker_odds
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Ошибка при сохранении матчей в базу данных: {str(e)}")
            return {
                'error': str(e)
            }
    
    @staticmethod
    def parse_and_save_all_matches():
        """
        Парсит матчи со всех источников и букмекеров, объединяет результаты и сохраняет в JSON и базу данных
        
        Returns:
            dict: Результат парсинга, объединения и сохранения
        """
        try:
            # Парсим матчи с источников
            source_result = ParserService.parse_matches_from_source()
            
            if source_result['status'] == 'error':
                logger.error(f"Ошибка при парсинге матчей с источников: {source_result['message']}")
                return {
                    'status': 'error',
                    'message': f'Ошибка при парсинге матчей с источников: {source_result["message"]}'
                }
            
            # Парсим матчи с букмекеров
            bookmaker_result = ParserService.parse_bookmaker_matches()
            
            if bookmaker_result['status'] == 'error':
                logger.error(f"Ошибка при парсинге матчей с букмекеров: {bookmaker_result['message']}")
                return {
                    'status': 'error',
                    'message': f'Ошибка при парсинге матчей с букмекеров: {bookmaker_result["message"]}'
                }
            
            # Объединяем результаты
            merge_result = ParserService.compare_and_merge_matches(
                source_result['matches'],
                bookmaker_result['matches']
            )
            
            if merge_result['status'] == 'error':
                logger.error(f"Ошибка при объединении матчей: {merge_result['message']}")
                return {
                    'status': 'error',
                    'message': f'Ошибка при объединении матчей: {merge_result["message"]}'
                }
            
            # Формируем сообщение о результатах сохранения в базу данных
            db_result = merge_result.get('db_result', {})
            db_message = ""
            
            if 'error' in db_result:
                db_message = f"Ошибка при сохранении в базу данных: {db_result['error']}"
            else:
                db_message = (
                    f"Сохранено {db_result.get('saved_matches', 0)} новых матчей, "
                    f"обновлено {db_result.get('updated_matches', 0)} существующих матчей. "
                    f"Сохранено {db_result.get('saved_source_odds', 0)} коэффициентов из источников и "
                    f"{db_result.get('saved_bookmaker_odds', 0)} коэффициентов из букмекеров."
                )
            
            return {
                'status': 'success',
                'message': f'Успешно спарсировано {source_result["matches_count"]} матчей с источников и {bookmaker_result["matches_count"]} матчей с букмекеров. Объединено {merge_result["merged_matches"]} матчей. {db_message}',
                'source_matches': source_result['matches_count'],
                'bookmaker_matches': bookmaker_result['matches_count'],
                'merged_matches': merge_result['merged_matches'],
                'merged_file': merge_result['merged_file'],
                'db_result': db_result
            }
            
        except Exception as e:
            logger.error(f"Ошибка при парсинге и объединении матчей: {str(e)}")
            return {
                'status': 'error',
                'message': f'Ошибка при парсинге и объединении матчей: {str(e)}'
            } 