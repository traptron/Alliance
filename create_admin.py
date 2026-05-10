from werkzeug.security import generate_password_hash

from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():

    hashed_password = generate_password_hash(
        "admin123"
    )

    user = User(
        username="admin",
        password=hashed_password
    )

    db.session.add(user)

    db.session.commit()

    print("Admin created!")