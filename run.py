import os
from dotenv import load_dotenv
from app import create_app, db

# Load environment variables from .env file
load_dotenv()

# Select config based on FLASK_ENV
config_name = os.getenv('FLASK_CONFIG') or ('production' if os.getenv('FLASK_ENV') == 'production' else 'default')
app = create_app(config_name)

if __name__ == '__main__':
    # Ensure tables are created for local development
    with app.app_context():
        db.create_all()
    
    # Run the application (Local use only - Gunicorn for Production)
    app.run(
        host='0.0.0.0', # Allows access from other devices in the local network
        port=int(os.getenv('PORT', 5000)),
        debug=app.config.get('DEBUG', False)
    )
