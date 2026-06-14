# This script is used to create an admin user in the database. Run it once before starting the application.
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))

from database import SessionLocal, engine, Base
from models import User
from auth import hash_password

Base.metadata.create_all(bind=engine)

username = input("Username: ")
password = input("Password: ")

db = SessionLocal()

if db.query(User).filter(User.username == username).first():
    print(f"User '{username}' already exists.")
    db.close()
    sys.exit(1)

user = User(username=username, password_hash=hash_password(password), role="admin")
db.add(user)
db.commit()
db.close()

print(f"Admin user '{username}' created.")
