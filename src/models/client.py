import enum
import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()


class Plan(enum.Enum):
    EMPRESARIO = 1
    EMPRENDEDOR = 2
    EMPRENDEDOR_PLUS = 3
    
class Rol(enum.Enum):
    AGENTE = 1,
    CLIENTE = 2


class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String, unique=True, nullable=False)
    id_number = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, default='')
    phoneNumber = db.Column(db.String, default='')
    plan = db.Column(db.Enum(Plan), default=Plan.EMPRESARIO)
    rol = db.Column(db.String, default='client')
    company = db.Column(db.String, default='')


class EnumToDictionary(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {"llave": value.name, "valor": value.value}


class ClientSchema(SQLAlchemyAutoSchema):
    plan = EnumToDictionary(attribute=('plan'))
    rol = EnumToDictionary(attribute=('rol'))
    
    class Meta:
        model = Client
        include_relationships = True
        load_instance = True