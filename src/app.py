from flask import Flask
from db.session import db_session


def create_app() -> Flask:
    app = Flask(__name__)

    @app.teardown_appcontext
    def shutdown_db_session(exception: Exception | None = None) -> None:
        print(f"shutdown_db_session({exception})")
        db_session.remove()

    from apps.gin_scoring import blueprint

    app.register_blueprint(blueprint.bp)

    return app
