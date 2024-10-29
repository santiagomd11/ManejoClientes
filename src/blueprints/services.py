from flask import Blueprint, request, jsonify
from src.commands.create_client import CreateClient

from src.commands.update_plan import UpdateClientPlan
from src.commands.get_client import GetClient
from src.commands.ping import Ping
from src.commands.clear_database import ClearDatabase

from src.errors.errors import BadRequest, NotFound


services_bp = Blueprint('services', __name__)

@services_bp.route('/create_client', methods=['POST'])
def create_client():
    json_input = request.get_json()
    command = CreateClient(json_input)
    response = command.execute()
    return jsonify(response), 201

@services_bp.route('/update_client_plan', methods=['PUT'])
def update_client_plan():
    json_input = request.get_json()
    command = UpdateClientPlan(json_input)
    command.execute()
    return jsonify({'message': 'Client plan updated successfully'}), 200

@services_bp.route('/get_client/<client_id>', methods=['GET'])
def get_client(client_id):
    command = GetClient(client_id)
    response = command.execute()
    return jsonify(response), 200

@services_bp.route('/clear_database', methods=['POST'])
def clear_database():
    command = ClearDatabase()
    command.execute()
    return jsonify({'message': 'Database cleared successfully'}), 200

@services_bp.route('/ping', methods=['GET'])
def ping():
    command = Ping()
    return jsonify({'message': command.execute()}), 200