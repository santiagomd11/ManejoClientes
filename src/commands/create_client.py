from src.commands.base_command import BaseCommand
from src.errors.errors import BadRequest, PreconditionFailed
from src.models.client import Client, db, Plan, Rol, IdType
import validators
import uuid

class CreateClient(BaseCommand):
    def __init__(self, json):
        self.id = json.get('id', '')
        self.id_type = json.get('idType', IdType.CEDULA_CIUDADANIA)
        self.name = json.get('name', '').strip()
        self.email = json.get('email', '').strip().lower()
        self.id_number = json.get('idNumber', '').strip()
        self.phone_number = json.get('phoneNumber', '').strip()
        self.plan = json.get('plan', Plan.EMPRESARIO)
        self.rol = json.get('rol', Rol.CLIENTE)
        self.company = json.get('company', '')

    def execute(self):
        if not self.id:
            raise BadRequest('Id is required')
        
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

        if not self.id_type:
            raise BadRequest('Id type is required')

        try:
            client = Client(
                id=self.id,
                name=self.name,
                id_type=self.id_type,
                id_number=self.id_number,
                email=self.email,
                phoneNumber=self.phone_number,
                plan=self.plan,
                rol=self.rol,
                company=self.company
            )

            db.session.add(client)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise PreconditionFailed("Failed to create client verify the data or if the client already exists")
        
        return {"id": self.id, "email": self.email}

def salt_password(password):
    salt = uuid.uuid4().hex
    salted_password = password + salt
    return {'password': salted_password, 'salt': salt}