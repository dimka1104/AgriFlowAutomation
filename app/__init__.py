import click
from flask import Flask

from app.config import Config
from app.extensions import db, login_manager


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from app.auth.routes import auth_bp
    from app.main.routes import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    with app.app_context():
        db.create_all()

    register_cli(app)

    return app


def register_cli(app):
    @app.cli.command("create-user")
    @click.option("--username", required=True)
    @click.option("--password", required=True)
    @click.option("--role", type=click.Choice(["master", "user"]), default="user")
    def create_user(username, password, role):
        """Create a new user (e.g. flask create-user --username admin --password secret --role master)."""
        from app.models import User

        if User.query.filter_by(username=username).first():
            click.echo(f"User '{username}' already exists.")
            return

        user = User(username=username, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo(f"Created {role} user '{username}'.")
