import os
from flask import Flask, redirect, url_for, session
from dotenv import load_dotenv
from extensions import db, bcrypt, login_manager, mail
from models import User, Branch

# Blueprints
from routes.auth import auth_bp
from routes.main import main_bp
from routes.sales import sales_bp
from routes.inventory import inventory_bp
from routes.customers import customers_bp
from routes.reports import reports_bp
from routes.users import users_bp

def create_app():
    app = Flask(__name__)

    load_dotenv()

    # =========================
    # CORE CONFIG
    # =========================
    SECRET_KEY = os.getenv('SECRET_KEY')
    DATABASE_URL = os.getenv('DATABASE_URL')

    if not SECRET_KEY:
        raise Exception("SECRET_KEY is missing in Vercel environment variables")

    if not DATABASE_URL:
        raise Exception("DATABASE_URL is missing in Vercel environment variables")

    app.config['SECRET_KEY'] = SECRET_KEY

    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_pre_ping": True,
        "connect_args": {
            "sslmode": "require"
        }
    }


    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # =========================
    # EMAIL CONFIG
    # =========================
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() in ['true', '1', 't']
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv(
        'MAIL_DEFAULT_SENDER',
        os.getenv('MAIL_USERNAME')
    )

    # =========================
    # EXTENSIONS
    # =========================
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # =========================
    # BLUEPRINTS
    # =========================
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(sales_bp, url_prefix='/sales')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(reports_bp, url_prefix='/reports')
    app.register_blueprint(users_bp, url_prefix='/users')

    @app.context_processor
    def inject_branches():
        from flask_login import current_user
        if current_user.is_authenticated:
            active_branch_id = session.get('active_branch_id')
            active_branch = Branch.query.get(active_branch_id) if active_branch_id else None

            all_branches = Branch.query.all() if current_user.role == 'admin' else []

            return dict(
                active_branch=active_branch,
                available_branches=all_branches
            )
        return dict()

    @app.route('/')
    def index():
        return redirect(url_for('main.dashboard'))

    return app


# =========================
# VERCEL ENTRY POINT
# =========================
app = create_app()

if __name__ == '__main__':
    with app.app_context():
        pass
    app.run(debug=True)

with app.app_context():
    from extensions import db
    try:
        db.session.execute("SELECT 1")
        print("DATABASE OK")
    except Exception as e:
        print("DATABASE FAILED:", e)