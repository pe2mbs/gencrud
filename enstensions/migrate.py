from flask_migrate import Migrate
import webapp.api as API

API.migrate = Migrate()
