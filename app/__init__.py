from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'secret'
app.config.from_object(Config)

db = SQLAlchemy(app)
db.create_all()
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

CORS(app)
from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
