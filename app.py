from flask import Flask, render_template
from backend.config.database import init_db
from backend.routes.web import web_bp
from backend.routes.api import api_bp
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app = Flask(__name__,
            template_folder="frontend/templates",
            static_folder="frontend/static")

app.config.from_object('backend.config.config.DevelopmentConfig')

app.secret_key = 'Mera_Namm_Prince_Kumar'


# Initialize MongoDB
init_db(app)

# Register Blueprints (no prefix for web)
app.register_blueprint(web_bp)
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True)
