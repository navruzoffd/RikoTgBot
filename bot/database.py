from sqlalchemy.orm import relationship
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String,
    Boolean,
    ForeignKey,
    DateTime
)

from sqlalchemy.ext.asyncio import (create_async_engine,
                                    async_sessionmaker,
                                    AsyncSession)

from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import make_url

from bot.core.config import settings

DATABASE_URL = str(settings.DATABASE_URL)
url = make_url(DATABASE_URL)

async_engine = create_async_engine(url)
Base_a = declarative_base()

class Base(Base_a):
    __abstract__ = True

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


metadata = Base.metadata


SessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(BigInteger, nullable=False, unique=True)
    username = Column(String, nullable=False)
    referrer = Column(BigInteger)
    points = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    complete_tasks = Column(Boolean, default=False)
    tg_premium = Column(Boolean, nullable=False)

    admin = relationship('Admin', back_populates='user')

class Admin(Base):
    __tablename__ = 'admin'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True, nullable=False)

    user = relationship('User', back_populates='admin')