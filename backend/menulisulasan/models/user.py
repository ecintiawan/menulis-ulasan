from menulisulasan import db, logger
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now())
    modified_at = db.Column(db.DateTime(), onupdate=datetime.now())
    is_delete = db.Column(db.Boolean(), default=False, nullable=False)

    def __init__(self, first_name, last_name, email, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)

    def __repr__(self):
        return str(self.json())

    def json(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "username": self.username
        }

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save_to_db(self):
        logger.info("START SAVE TO DB")
        db.session.add(self)
        db.session.commit()
        logger.info("END SAVE TO DB")

    def delete_from_db(self):
        logger.info("START DELETE FROM DB")
        self.is_delete = True
        db.session.commit()
        logger.info("END DELETE FROM DB")

    def update_data_to_db(self, first_name, last_name, email, username):
        logger.info("START UPDATE TO DB")
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        db.session.commit()
        logger.info("END UPDATE TO DB")

    def update_password_to_db(self, password):
        logger.info("START UPDATE TO DB")
        self.password = generate_password_hash(password)
        db.session.commit()
        logger.info("END UPDATE TO DB")

    @classmethod
    def find_by_username(cls, username):
        logger.info("START GET DATA FROM DB")
        user = cls.query.filter_by(username=username, is_delete=False).first()
        logger.info("END GET DATA FROM DB")
        return user

    @classmethod
    def find_by_email(cls, email):
        logger.info("START GET DATA FROM DB")
        user = cls.query.filter_by(email=email, is_delete=False).first()
        logger.info("END GET DATA FROM DB")
        return user

    @classmethod
    def find_by_id(cls, _id):
        logger.info("START GET DATA FROM DB")
        user = cls.query.filter_by(id=_id, is_delete=False).first()
        logger.info("END GET DATA FROM DB")
        return user
