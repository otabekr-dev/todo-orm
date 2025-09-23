from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey
)

from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64))
    email = Column(String(64), nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)

    tasks = relationship('Task', back_populates='user')


    @property
    def full_name(self) -> str:
        if self.last_name:
            return f'{self.first_name} {self.last_name}'
        return {self.first_name}

    def __repr__(self) -> str:
        return f'User(id={self.user_id}, name={self.email}, fullname={self.full_name})'


class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(Integer, primary_key = True)
    name = Column(String(128), nullable = False)
    description = Column(Text)
    user_id = Column(ForeignKey('users.user_id', on_delete = 'CASCADE'))

    user = relationship('User', back_populates = 'tasks')

    def __repr__(self) -> str:
        return f"Task(id={self.task_id}, name={self.name}, user={self.user.full_name})"