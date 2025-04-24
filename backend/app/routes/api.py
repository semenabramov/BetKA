from flask import Blueprint, jsonify, request
from app.core.database import db
from app.services.match_service import MatchService
from app.services.alias_service import AliasService
from sqlalchemy import text
from app.models.bookmaker import Bookmaker
from app.models.team import Team
from app.services.odds_source_service import OddsSourceService
from app.services.odds_service import OddsService
from app.models.odds import BookmakerOdds
from app.models.odds import OddsFromSource
from app.models.match import Match
from app.services.parser_service import ParserService

bp = Blueprint('api', __name__)

@bp.route('/health', methods=['GET'])
def health_check():
    """Проверка работоспособности сервера"""
    return jsonify({
        'status': 'success',
        'message': 'Server is running'
    })

@bp.route('/db-check', methods=['GET'])
def db_check():
    """Проверка подключения к базе данных"""
    try:
        # Пробуем выполнить простой запрос
        db.session.execute(text('SELECT 1'))
        return jsonify({
            'status': 'success',
            'message': 'Database connection is working'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Database connection error: {str(e)}'
        }), 500

@bp.route('/matches', methods=['GET'])
def get_matches():
    """Получение списка всех матчей с коэффициентами"""
    matches = MatchService.get_all_matches()
    return jsonify(matches)

@bp.route('/matches', methods=['POST'])
def create_match():
    """Создание нового матча"""
    try:
        match_data = request.get_json()
        match = MatchService.create_match(match_data)
        
        if match:
            return jsonify({
                'status': 'success',
                'message': 'Match created successfully',
                'data': match.to_dict()
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to create match'
            }), 400
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bp.route('/matches/mock', methods=['GET'])
def create_mock_match():
    """Создание тестового матча"""
    try:
        match = MatchService.create_mock_match()
        
        if match:
            return jsonify({
                'status': 'success',
                'message': 'Mock match created successfully',
                'data': match.to_dict()
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to create mock match'
            }), 400
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bp.route('/teams', methods=['POST'])
def create_team():
    """Создание новой команды"""
    try:
        data = request.get_json()
        team = MatchService.create_team(
            name=data['name'],
            league=data['league']
        )
        
        if team:
            return jsonify({
                'status': 'success',
                'message': 'Team created successfully',
                'data': {
                    'id': team.id,
                    'name': team.name,
                    'league': team.league
                }
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to create team'
            }), 400
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bp.route('/teams', methods=['GET'])
def get_teams():
    """Получение списка всех команд с альтернативными названиями"""
    teams = MatchService.get_all_teams()
    return jsonify({
        'status': 'success',
        'data': teams
    })

@bp.route('/teams/<int:team_id>/aliases', methods=['GET'])
def get_team_aliases(team_id):
    """Получение альтернативных названий команды"""
    aliases = AliasService.get_aliases_by_team_id(team_id)
    return jsonify({
        'status': 'success',
        'data': [alias.to_dict() for alias in aliases]
    })

@bp.route('/teams/<int:team_id>/aliases', methods=['POST'])
def add_team_alias(team_id):
    """Добавление альтернативного названия для команды"""
    try:
        data = request.get_json()
        alias = AliasService.add_alias(
            team_id=team_id, 
            alias=data['alias'],
            language=data.get('language', 'ru')
        )
        
        if alias:
            return jsonify({
                'status': 'success',
                'message': 'Alias added successfully',
                'data': alias.to_dict()
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to add alias'
            }), 400
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bp.route('/teams/aliases/<int:alias_id>', methods=['DELETE'])
def delete_team_alias(alias_id):
    """Удаление альтернативного названия"""
    success = AliasService.delete_alias(alias_id)
    
    if success:
        return jsonify({
            'status': 'success',
            'message': 'Alias deleted successfully'
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'Failed to delete alias'
        }), 400

@bp.route('/bookmakers', methods=['GET'])
def get_bookmakers():
    """Получение списка всех букмекеров"""
    bookmakers = Bookmaker.query.all()
    return jsonify({
        'status': 'success',
        'data': [bookmaker.to_dict() for bookmaker in bookmakers]
    })

@bp.route('/bookmakers', methods=['POST'])
def create_bookmaker():
    """Создание нового букмекера"""
    try:
        data = request.get_json()
        bookmaker = Bookmaker(
            name=data['name'],
            premier_league_url=data.get('premier_league_url'),
            championship_url=data.get('championship_url'),
            league_one_url=data.get('league_one_url'),
            league_two_url=data.get('league_two_url'),
            bundesliga_one_url=data.get('bundesliga_one_url'),
            bundesliga_two_url=data.get('bundesliga_two_url'),
            liga_url=data.get('liga_url'),
            la_liga_url=data.get('la_liga_url'),
            serie_a_url=data.get('serie_a_url'),
            ligue_one_url=data.get('ligue_one_url')
        )
        
        db.session.add(bookmaker)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Bookmaker created successfully',
            'data': bookmaker.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bp.route('/bookmakers/<int:bookmaker_id>', methods=['PUT'])
def update_bookmaker(bookmaker_id):
    """Обновление букмекера"""
    try:
        bookmaker = Bookmaker.query.get_or_404(bookmaker_id)
        data = request.get_json()
        
        bookmaker.name = data.get('name', bookmaker.name)
        bookmaker.premier_league_url = data.get('premier_league_url', bookmaker.premier_league_url)
        bookmaker.championship_url = data.get('championship_url', bookmaker.championship_url)
        bookmaker.league_one_url = data.get('league_one_url', bookmaker.league_one_url)
        bookmaker.league_two_url = data.get('league_two_url', bookmaker.league_two_url)
        bookmaker.bundesliga_one_url = data.get('bundesliga_one_url', bookmaker.bundesliga_one_url)
        bookmaker.bundesliga_two_url = data.get('bundesliga_two_url', bookmaker.bundesliga_two_url)
        bookmaker.liga_url = data.get('liga_url', bookmaker.liga_url)
        bookmaker.la_liga_url = data.get('la_liga_url', bookmaker.la_liga_url)
        bookmaker.serie_a_url = data.get('serie_a_url', bookmaker.serie_a_url)
        bookmaker.ligue_one_url = data.get('ligue_one_url', bookmaker.ligue_one_url)
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Bookmaker updated successfully',
            'data': bookmaker.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bp.route('/bookmakers/<int:bookmaker_id>', methods=['DELETE'])
def delete_bookmaker(bookmaker_id):
    """Удаление букмекера"""
    try:
        bookmaker = Bookmaker.query.get_or_404(bookmaker_id)
        
        # Сначала удаляем все связанные записи из таблицы Bookmakers_odds
        BookmakerOdds.query.filter_by(bookmaker_id=bookmaker_id).delete()
        
        # Теперь можно удалить самого букмекера
        db.session.delete(bookmaker)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Букмекер успешно удален'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@bp.route('/teams/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    """Удаление команды"""
    try:
        team = Team.query.get(team_id)
        if not team:
            return jsonify({
                'status': 'error',
                'message': 'Team not found'
            }), 404
        
        db.session.delete(team)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Team deleted successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Маршруты для источников коэффициентов
@bp.route('/odds-sources', methods=['GET'])
def get_odds_sources():
    sources = OddsSourceService.get_all_sources()
    return jsonify([source.to_dict() for source in sources])

@bp.route('/odds-sources/<int:source_id>', methods=['GET'])
def get_odds_source(source_id):
    source = OddsSourceService.get_source_by_id(source_id)
    if not source:
        return jsonify({'error': 'Source not found'}), 404
    return jsonify(source.to_dict())

@bp.route('/odds-sources', methods=['POST'])
def create_odds_source():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        required_fields = ['name', 'url']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
                
        source = OddsSourceService.create_source(data)
        return jsonify(source.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/odds-sources/<int:source_id>', methods=['PUT'])
def update_odds_source(source_id):
    data = request.get_json()
    source = OddsSourceService.update_source(source_id, data)
    if not source:
        return jsonify({'error': 'Source not found'}), 404
    return jsonify(source.to_dict())

@bp.route('/odds-sources/<int:source_id>', methods=['DELETE'])
def delete_odds_source(source_id):
    success = OddsSourceService.delete_source(source_id)
    if not success:
        return jsonify({'error': 'Source not found'}), 404
    return '', 204

# Маршруты для коэффициентов из источников
@bp.route('/matches/<int:match_id>/source-odds', methods=['GET'])
def get_match_source_odds(match_id):
    odds = OddsService.get_odds_by_match_id(match_id)
    return jsonify([odd.to_dict() for odd in odds])

@bp.route('/matches/<int:match_id>/source-odds', methods=['POST'])
def create_match_source_odds(match_id):
    data = request.get_json()
    source_id = data.get('source_id')
    if not source_id:
        return jsonify({'error': 'Source ID is required'}), 400
        
    odds = OddsService.create_source_odds(match_id, source_id, data)
    return jsonify(odds.to_dict()), 201

@bp.route('/source-odds/<int:odds_id>', methods=['PUT'])
def update_match_source_odds(odds_id):
    data = request.get_json()
    odds = OddsService.update_source_odds(odds_id, data)
    if not odds:
        return jsonify({'error': 'Odds not found'}), 404
    return jsonify(odds.to_dict())

@bp.route('/source-odds/<int:odds_id>', methods=['DELETE'])
def delete_match_source_odds(odds_id):
    success = OddsService.delete_source_odds(odds_id)
    if not success:
        return jsonify({'error': 'Odds not found'}), 404
    return '', 204

@bp.route('/matches/<int:match_id>', methods=['DELETE'])
def delete_match(match_id):
    """Удаление матча по ID"""
    try:
        match = Match.query.get(match_id)
        if not match:
            return jsonify({'status': 'error', 'message': 'Матч не найден'}), 404
        
        # Удаляем связанные коэффициенты
        OddsFromSource.query.filter_by(match_id=match_id).delete()
        BookmakerOdds.query.filter_by(match_id=match_id).delete()
        
        # Удаляем сам матч
        db.session.delete(match)
        db.session.commit()
        
        return jsonify({'status': 'success', 'message': 'Матч успешно удален'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/matches/update-all', methods=['POST'])
def update_all_matches():
    """Запускает процесс парсинга матчей со всех источников и букмекеров, объединяет результаты и сохраняет в JSON"""
    try:
        result = ParserService.parse_and_save_all_matches()
        
        if result['status'] == 'success':
            return jsonify({
                'status': 'success',
                'message': result['message'],
                'source_matches': result['source_matches'],
                'bookmaker_matches': result['bookmaker_matches'],
                'merged_matches': result['merged_matches'],
            })
        else:
            return jsonify({
                'status': 'error',
                'message': result['message']
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Ошибка при обновлении матчей: {str(e)}'
        }), 500 