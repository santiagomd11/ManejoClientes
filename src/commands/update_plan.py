from src.commands.base_command import BaseCommand
from src.errors.errors import NotFound, BadRequest
from src.models.client import Client, db, Plan

class UpdateClientPlan(BaseCommand):
    def __init__(self, json_input):
        self.company = json_input.get('company')
        self.new_plan = json_input.get('plan')
        try:
            self.new_plan = Plan[self.new_plan]
        except KeyError:
            raise BadRequest('Invalid plan')

    def execute(self):
        try:
            clients = Client.query.filter_by(company=self.company).all()
            if not clients:
                raise NotFound(f'No clients found for company {self.company}')

            for client in clients:
                client.plan = self.new_plan

            db.session.commit()

        except NotFound as e:
            raise e
        
        except Exception as e:
            db.session.rollback()
            raise e