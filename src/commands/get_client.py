from src.commands.base_command import BaseCommand
from src.errors.errors import NotFound
from src.models.client import Client, db

class GetClient(BaseCommand):
    def __init__(self, client_id):
        self.client_id = client_id

    def execute(self):
        try:
            client = Client.query.filter_by(id=self.client_id).first()
            if not client:
                raise NotFound(f'Client with id {self.client_id} not found')

            client_info = {
                'id': client.id,
                'name': client.name,
                'email': client.email,
                'id_number': client.id_number,
                'phoneNumber': client.phoneNumber,
                'plan': client.plan.name,
                'rol': client.rol,
                'company': client.company
            }

            return client_info

        except Exception as e:
            db.session.rollback()
            raise e