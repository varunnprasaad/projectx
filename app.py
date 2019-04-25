from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://varun:0000@localhost/roadrunner'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "somesecretkey"

# Add Bootstrap
Bootstrap(app)

# Add Sqlalchemy
db = SQLAlchemy(app)

# Flask Login
login_manager = LoginManager(app)

'''
    Redirect user to login page (auth.login), if user is not authenticated
'''
login_manager.login_view = 'auth.login'

import db_handler.models


@login_manager.user_loader
def load_user(user_id):
    return db_handler.models.Customer.query.get(int(user_id))


from auth import auth as auth_blueprint

app.register_blueprint(auth_blueprint)

from main import main as main_blueprint

app.register_blueprint(main_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
