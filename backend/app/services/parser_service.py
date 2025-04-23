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
from sqlalchemy import or_
from app.models.alias_team import AliasTeam

logger = logging.getLogger(__name__)

class ParserService:
    @staticmethod
    def parse_matches_from_source(source_id=None):
        """
        Парсит матчи с указанного источника или всех активных источников
        
        Args:
            source_id (int, optional): ID источника для парсинга. Если None, парсит все активные источники.
            
        Returns:
            dict: Результат парсинга с информацией о количестве обработанных матчей
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
                    'message': 'Нет активных источников для парсинга'
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
                logger.info(f"URL лиг: {league_urls}")
                
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
                        total_matches += len(matches)
                        results.extend(matches)
                        logger.info(f"Успешно спарсили {len(matches)} матчей с {url}")
                    except Exception as e:
                        logger.error(f"Ошибка при парсинге {url}: {str(e)}")
            
            # Сохраняем результаты в JSON файл
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"parsed_matches_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
                
            logger.info(f"Сохранено {len(results)} матчей в файл {filename}")
            
            return {
                'status': 'success',
                'message': f'Успешно спарсировано {total_matches} матчей',
                'filename': filename,
                'matches_count': total_matches
            }
            
        except Exception as e:
            logger.error(f"Ошибка при парсинге матчей: {str(e)}")
            return {
                'status': 'error',
                'message': f'Ошибка при парсинге матчей: {str(e)}'
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