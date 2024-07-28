from sqlalchemy import Column, String, DateTime, Boolean, Integer
from database.connection import Base

class Users(Base):
     
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    user_id = Column('user_id', String(32), primary_key=True, nullable=False)
    username = Column('username', String(100), nullable=False)
    first_name = Column('first_name', String(50), nullable=False)
    middle_name = Column('middle_name', String(50), nullable=True)
    last_name = Column('last_name', String(50), nullable=False)
    email = Column('email', String(320), nullable=True)
    gender = Column('gender', String(6), nullable=True)
    age = Column('age', Integer, nullable=True)
    bio = Column('bio', String(320), nullable=True)
    preferences = Column('preferences', String(320), nullable=True)
    created_on = Column('created_on', DateTime, nullable=False)
    is_active = Column('is_active', Boolean, nullable=False)
    deactivated_on = Column('deactivated_on', DateTime, nullable=True)
    otp = Column(Integer, nullable=True)
    otp_generated_on = Column(DateTime, nullable=True)


