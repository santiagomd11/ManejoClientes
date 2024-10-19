from src.commands.base_command import BaseCommand
from src.errors.errors import NotFound, BadRequest
from src.models.client import Client, db, Plan

class UpdateClientPlan(BaseCommand):
    def __init__(self, json_input):
        self.client_email = json_input.get('email')
        self.new_plan = json_input.get('plan')
        try:
            self.new_plan = Plan[self.new_plan]
        except KeyError:
            raise BadRequest('Invalid plan')

    def execute(self):
        try:
            client = Client.query.filter_by(email=self.client_email).first()
            if not client:
                raise NotFound(f'Client not found')

            if not isinstance(self.new_plan, Plan):
                raise BadRequest('Invalid plan')

            client.plan = self.new_plan
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise e