from flask import Blueprint, jsonify, request
from app.core.database import db
from app.services.match_service import MatchService
from app.services.alias_service import AliasService
from sqlalchemy import text

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
    """Получение списка всех матчей"""
    matches = MatchService.get_all_matches()
    return jsonify({
        'status': 'success',
        'data': [match.to_dict() for match in matches]
    })

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
    """Получение списка всех команд"""
    teams = MatchService.get_all_teams()
    return jsonify({
        'status': 'success',
        'data': [team.to_dict() for team in teams]
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