from application import db
from application.models import Data, Image

db.create_all()

print("DB created.")
