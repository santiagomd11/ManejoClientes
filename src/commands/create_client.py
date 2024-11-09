from src.commands.base_command import BaseCommand
from src.errors.errors import BadRequest, PreconditionFailed
from src.models.client import Client, db, Plan, Rol, IdType
import validators
import uuid

import logging
import os

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

class CreateClient(BaseCommand):
    def __init__(self, json):
        self.id = json.get('id', '')
        self.id_type = json.get('idType', IdType.CEDULA_CIUDADANIA)
        self.name = json.get('name', '').strip()
        self.email = json.get('email', '').strip().lower()
        self.id_number = json.get('idNumber', '').strip()
        self.phone_number = json.get('phoneNumber', '').strip()
        self.plan = json.get('plan', Plan.EMPRENDEDOR)
        self.rol = json.get('rol', Rol.CLIENTE)
        self.company = json.get('company', '')
        logger.info(f"client info: {json}")
        logger.info(f"client rol: {self.rol}, type: {type(self.rol)}")
    
    def validate_clients_for_company(self, company):
        clients = Client.query.filter(
            (Client.company == company) & (Client.rol == Rol.CLIENTE)
        ).all()
        
        logger.info(f"clients found: {clients}")
        
        if clients:
            raise PreconditionFailed(f"There's already a client for the company {company}")

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
        
        if self.rol == Rol.CLIENTE.name:
            self.validate_clients_for_company(self.company)

        try:
            client = Client(
                id=self.id,
                name=self.name,
                id_type=self.id_type,
                id_number=self.id_number,
                email=self.email,
                phoneNumber=self.phone_number,
                plan=self.plan if self.plan else Plan.EMPRENDEDOR,
                rol=self.rol,
                company=self.company
            )

            db.session.add(client)
            db.session.commit()

        except Exception as e:
            logger.info(f'Error creating client: {e}')
            db.session.rollback()
            raise PreconditionFailed("Failed to create client verify the data or if the client already exists")
        
        return {"id": self.id, "email": self.email}

def salt_password(password):
    salt = uuid.uuid4().hex
    salted_password = password + salt
    return {'password': salted_password, 'salt': salt}