from sqlalchemy import Column, Integer, String , ForeignKey , Date
from database.db import base

class Task(base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String , unique=True)
    description = Column(String)
    due_date = Column(Date, nullable=False)
    priority = Column(Integer, nullable=False)

class users(base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    password = Column(String)
    email = Column(String)

class TaskAttachment(base):
    __tablename__ = "task_attachments"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    filename = Column(String)
    



