import os
import traceback
from flask import Flask, jsonify
from src.models.client import db
from src.blueprints.services import services_bp

def create_app(config_name, local=False):
    app = Flask(__name__)
    app.register_blueprint(services_bp, url_prefix='/clients')

    db_uri = 'sqlite:///clients.db'
    try:
        if not local:
            db_host = os.environ.get('DB_HOST')
            db_port = os.environ.get('DB_PORT')
            db_name = os.environ.get('DB_NAME')
            db_user = os.environ.get('DB_USER')
            db_password = os.environ.get('DB_PASSWORD')

            if all([db_port, db_host, db_name, db_user, db_password]):
                db_uri = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    except Exception as e:
        print(f'Error connecting to db: {e}')
    finally:
        print(db_uri)

    app_context = app.app_context()
    app_context.push()
    db.init_app(app)
    db.create_all()

    return app

app = create_app('manejo-clientes')

@app.errorhandler(Exception)
def handle_exception(err):
    trace = traceback.format_exc()
    response = {
        "msg": getattr(err, 'description', str(err)),
        "traceback": trace
    }
    return jsonify(response), getattr(err, 'code', 500)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)