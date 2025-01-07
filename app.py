from flask import Flask
import config
from models import init_db
from data_manager.sqlite_data_manager import SQLiteDataManager

app = Flask(__name__)

app.config.from_object(config)

init_db(app)

data_manager = SQLiteDataManager()

@app.route('/')
def home():
    return "Welcome to MovieWeb App!"

@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return str(users)  # Temporarily returning users as a string

if __name__ == '__main__':
    app.run(debug=True)
