import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import logging
import os

logger = logging.getLogger(__name__)

class MatchResultParser:
    
    @staticmethod
    def parse_championat_results(url: str, league: str) -> list:
        """
        Парсит результаты матчей с Championat.com
        
        Args:
            url: URL страницы с календарем
            league: Название лиги
            
        Returns:
            list: Список распарсенных матчей
        """
        try:
            logger.info(f"Начинаем парсинг результатов с {url}")
            
            # Получаем HTML страницы
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Парсим HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Ищем таблицу с результатами
            results_table = soup.find('tbody')
            if not results_table:
                logger.warning("Таблица с результатами не найдена")
                return []
            
            # Парсим каждую строку с матчем
            matches = []
            rows = results_table.find_all('tr', class_='stat-results__row')
            
            logger.info(f"Найдено {len(rows)} строк с матчами")
            
            for row in rows:
                try:
                    match_data = MatchResultParser._parse_match_row(row, league)
                    if match_data:
                        matches.append(match_data)
                        logger.info(f"Распарсен матч: {match_data['home_team']} - {match_data['away_team']} {match_data['score']}")
                except Exception as e:
                    logger.error(f"Ошибка при парсинге строки: {e}")
                    continue
            
            logger.info(f"Успешно распарсено {len(matches)} матчей")
            return matches
            
        except Exception as e:
            logger.error(f"Ошибка при парсинге {url}: {e}")
            return []
    
    @staticmethod
    def update_match_scores_in_database(parsed_matches: list) -> dict:
        """
        Сопоставляет распарсенные матчи с матчами в базе данных и обновляет результаты
        
        Args:
            parsed_matches: Список распарсенных матчей
            
        Returns:
            dict: Статистика обновления
        """
        from app.models.match import Match
        from app.models.team import Team
        from app.core.database import db
        
        stats = {
            'total_parsed': len(parsed_matches),
            'matched': 0,
            'updated': 0,
            'not_found': 0,
            'errors': 0,
            'details': []
        }
        
        logger.info(f"Начинаем сопоставление {len(parsed_matches)} распарсенных матчей")
        
        for parsed_match in parsed_matches:
            try:
                # Ищем соответствующий матч в базе данных
                db_match = MatchResultParser._find_matching_match(parsed_match)
                
                if not db_match:
                    stats['not_found'] += 1
                    stats['details'].append({
                        'parsed_match': parsed_match,
                        'status': 'not_found',
                        'reason': 'Матч не найден в базе данных'
                    })
                    logger.warning(f"Матч не найден: {parsed_match['home_team']} - {parsed_match['away_team']} {parsed_match['date']}")
                    continue
                
                stats['matched'] += 1
                
                # Проверяем, нужно ли обновлять счет
                if db_match.match_score == parsed_match['score']:
                    stats['details'].append({
                        'parsed_match': parsed_match,
                        'db_match_id': db_match.id,
                        'status': 'no_change',
                        'reason': 'Счет уже актуальный'
                    })
                    logger.debug(f"Счет уже актуальный для матча {db_match.id}: {parsed_match['score']}")
                    continue
                
                # Обновляем счет
                old_score = db_match.match_score
                db_match.match_score = parsed_match['score']
                db.session.commit()
                
                stats['updated'] += 1
                stats['details'].append({
                    'parsed_match': parsed_match,
                    'db_match_id': db_match.id,
                    'status': 'updated',
                    'old_score': old_score,
                    'new_score': parsed_match['score']
                })
                
                logger.info(f"Обновлен счет матча {db_match.id}: {old_score} -> {parsed_match['score']}")
                
            except Exception as e:
                stats['errors'] += 1
                stats['details'].append({
                    'parsed_match': parsed_match,
                    'status': 'error',
                    'error': str(e)
                })
                logger.error(f"Ошибка при обновлении матча {parsed_match}: {e}")
        
        logger.info(f"Сопоставление завершено. Статистика: {stats}")
        return stats
    
    @staticmethod
    def _find_matching_match(parsed_match: dict):
        """
        Ищет соответствующий матч в базе данных
        
        Args:
            parsed_match: Распарсенный матч
            
        Returns:
            Match: Найденный матч или None
        """
        from app.models.match import Match
        from app.models.team import Team
        from app.core.database import db
        
        # Парсим дату
        try:
            match_date = datetime.strptime(parsed_match['date'], '%Y-%m-%d')
        except ValueError:
            logger.error(f"Неверный формат даты: {parsed_match['date']}")
            return None
        
        # Ищем команды по названию
        home_team = MatchResultParser._find_team_by_name(parsed_match['home_team'])
        away_team = MatchResultParser._find_team_by_name(parsed_match['away_team'])
        
        if not home_team or not away_team:
            logger.warning(f"Не найдены команды: {parsed_match['home_team']} или {parsed_match['away_team']}")
            return None
        
        # Ищем матч по командам и дате
        match = Match.query.filter(
            Match.team_home == home_team.id,
            Match.team_away == away_team.id,
            db.func.date(Match.date) == match_date.date()
        ).first()
        
        return match
    
    @staticmethod
    def _find_team_by_name(team_name: str):
        """
        Ищет команду по названию с учетом альтернативных названий
        
        Args:
            team_name: Название команды
            
        Returns:
            Team: Найденная команда или None
        """
        from app.models.team import Team
        from app.models.alias_team import AliasTeam
        
        # Сначала ищем точное совпадение в основной таблице команд
        team = Team.query.filter(Team.name == team_name).first()
        if team:
            logger.debug(f"Найдено точное совпадение в основной таблице: '{team_name}' -> '{team.name}'")
            return team
        
        # Ищем в альтернативных названиях
        alias = AliasTeam.query.filter(AliasTeam.alias_name == team_name).first()
        if alias:
            team = Team.query.get(alias.id_team)
            if team:
                logger.debug(f"Найдено совпадение в альтернативных названиях: '{team_name}' -> '{team.name}' (alias: {alias.alias_name})")
                return team
        
        logger.warning(f"Команда не найдена: '{team_name}'")
        return None
    
    @staticmethod
    def _parse_match_row(row, league: str) -> dict:
        """
        Парсит одну строку с матчем
        
        Args:
            row: BeautifulSoup элемент строки
            league: Название лиги
            
        Returns:
            dict: Данные матча или None
        """
        try:
            # Получаем команды
            teams_elements = row.find_all('span', class_='table-item__name')
            if len(teams_elements) < 2:
                logger.debug(f"Не найдено 2 команды в строке: {len(teams_elements)}")
                return None
                
            home_team = teams_elements[0].text.strip()
            away_team = teams_elements[1].text.strip()
            
            # Получаем дату
            date_element = row.find('td', class_='stat-results__date-time')
            if not date_element:
                logger.debug("Не найден элемент с датой")
                return None
                
            date_text = date_element.get_text(strip=True)
            # Убираем невидимые символы
            date_text = date_text.replace('\xa0', ' ').strip()
            match_date = MatchResultParser._parse_date(date_text)
            if not match_date:
                logger.debug(f"Не удалось распарсить дату: '{date_text}'")
                return None
            
            # Получаем счет
            score_element = row.find('span', class_='stat-results__count-main')
            if not score_element:
                logger.debug("Не найден элемент со счетом")
                return None
                
            score = score_element.get_text(strip=True)
            # Убираем невидимые символы
            score = score.replace('\xa0', ' ').strip()
            if not MatchResultParser._is_valid_score(score):
                logger.debug(f"Невалидный счет: '{score}'")
                return None
            
            match_data = {
                'home_team': home_team,
                'away_team': away_team,
                'date': match_date,
                'score': score,
                'source': 'Championat.com',
                'league': league
            }
            
            logger.debug(f"Успешно распарсен матч: {home_team} - {away_team} {score}")
            return match_data
            
        except Exception as e:
            logger.error(f"Ошибка при парсинге строки: {e}")
            return None
    
    @staticmethod
    def _parse_date(date_text: str) -> str:
        """
        Парсит дату из текста
        
        Args:
            date_text: Текст с датой (например: "01.08.2025 21:30")
            
        Returns:
            str: Дата в формате YYYY-MM-DD или None
        """
        try:
            # Убираем время, оставляем только дату
            date_part = date_text.split()[0]
            
            # Парсим дату в формате DD.MM.YYYY
            date_obj = datetime.strptime(date_part, '%d.%m.%Y')
            
            # Возвращаем в формате YYYY-MM-DD
            return date_obj.strftime('%Y-%m-%d')
            
        except Exception as e:
            logger.error(f"Ошибка при парсинге даты '{date_text}': {e}")
            return None
    
    @staticmethod
    def _is_valid_score(score: str) -> bool:
        """
        Проверяет валидность счета
        
        Args:
            score: Счет в формате "1 : 0" или "2:1"
            
        Returns:
            bool: True если счет валидный
        """
        if not score or score.strip() == '':
            return False
            
        # Убираем пробелы и приводим к единому формату
        clean_score = score.strip().replace(' ', '')
        
        # Проверяем формат "число:число"
        pattern = r'^\d+:\d+$'
        return bool(re.match(pattern, clean_score)) 