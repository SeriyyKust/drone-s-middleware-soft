from sqlalchemy import Boolean, Column, String

from src.database import Base


class TelegramUser(Base):
    __tablename__ = "telegram_users"

    id = Column(String(128), primary_key=True, index=True)
    able = Column(Boolean, default=True)

    def __repr__(self):
        return f"TelegramUser: {self.id} ({self.able})"

    def __str__(self):
        return f"TelegramUser: {self.id} ({self.able})"
