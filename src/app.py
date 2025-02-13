from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from src.views import views
import os

app = Flask(__name__)
# Set secret key from environment variable or use a default for development
app.secret_key = os.environ.get('SECRET_KEY', 'dev')
app.register_blueprint(views)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)