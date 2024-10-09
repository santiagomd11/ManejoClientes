from src.commands.base_command import BaseCommand
from src.errors.errors import BadRequest
from src.models.client import Client, db, Plan
import validators
import uuid

class CreateClient(BaseCommand):
    def __init__(self, json):
        self.name = json.get('name', '').strip()
        self.email = json.get('email', '').strip().lower()
        self.id_number = json.get('idNumber', '').strip()
        self.phone_number = json.get('phoneNumber', '').strip()
        self.plan = json.get('plan', Plan.EMPRESARIO)

    def execute(self):
        try:
            if not (self.name and self.password and self.email):
                raise BadRequest('Name, password, and email are required')

            valid_email = validators.email(self.email)
            if not valid_email:
                raise BadRequest('Invalid email format')

            client = Client(
                id=str(uuid.uuid4()),
                name=self.name,
                email=self.email,
                id_number=self.id_number,
                phoneNumber=self.phone_number,
                plan=self.plan
            )

            db.session.add(client)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise e

def salt_password(password):
    salt = uuid.uuid4().hex
    salted_password = password + salt
    return {'password': salted_password, 'salt': salt}