from datetime import datetime, timezone

from app.extensions.database import db


class User(db.db.Model):
    __tablename__ = "users"

    id = db.db.Column(db.db.Integer, primary_key=True)
    username = db.db.Column(db.db.String(32), unique=True, nullable=False)
    password = db.db.Column(db.db.String(255), nullable=False)
    created_at = db.db.Column(db.db.DateTime, default=datetime.utcnow)
    updated_at = db.db.Column(
        db.db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    @classmethod
    def create(cls, username: str, password: str):
        user = cls(username=username, password=password)
        db.db.session.add(user)
        db.db.session.commit()
        return user

    @classmethod
    def get_by_username(cls, username: str):
        return cls.query.filter_by(username=username).first()
