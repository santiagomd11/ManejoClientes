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
        self.rol = json.get('rol', 'client')
        self.company = json.get('company', '')

    def execute(self):
        try:
            if not (self.name and self.email):
                raise BadRequest('Name and email are required')

            valid_email = validators.email(self.email)
            if not valid_email:
                raise BadRequest('Invalid email format')

            if not self.id_number:
                raise BadRequest('Id is required')

            if not self.phone_number:
                raise BadRequest('Phone number is required')
            
            if not self.rol:
                raise BadRequest('Rol is required')

            if not self.company:
                raise BadRequest('Company is required')

            client_id = str(uuid.uuid4())
            client = Client(
                id=client_id,
                name=self.name,
                email=self.email,
                id_number=self.id_number,
                phoneNumber=self.phone_number,
                plan=self.plan,
                company=self.company
            )

            db.session.add(client)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise e
        
        return {"id": client_id, "email": self.email}

def salt_password(password):
    salt = uuid.uuid4().hex
    salted_password = password + salt
    return {'password': salted_password, 'salt': salt}