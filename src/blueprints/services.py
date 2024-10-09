from flask import Blueprint, request, jsonify
from commands.create_client import CreateClient
from src.commands.update_plan import UpdateClientPlan
from src.commands.ping import Ping
from src.errors.errors import BadRequest, NotFound

services_bp = Blueprint('services', __name__)

@services_bp.route('/create_client', methods=['POST'])
def create_client():
    try:
        json_input = request.get_json()
        command = CreateClient(json_input)
        command.execute()
        return jsonify({'message': 'Client created successfully'}), 201
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@services_bp.route('/update_client_plan', methods=['PUT'])
def update_client_plan():
    try:
        json_input = request.get_json()
        command = UpdateClientPlan(json_input)
        command.execute()
        return jsonify({'message': 'Client plan updated successfully'}), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@services_bp.route('/ping', methods=['GET'])
def ping():
    command = Ping()
    return jsonify({'message': command.execute()}), 200