from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Float,
    Table
)

from sqlalchemy.orm import relationship

from Database.database import Base


# association_table = Table(
#     'users_categories', Base.metadata,
#     Column('user_id', Integer, ForeignKey('users.id')),
#     Column('category_id', Integer, ForeignKey('categories.id'))
# )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    user_type = Column(Integer)
    # categories = relationship(
    #     "Category",
    #     secondary=association_table,
    #     back_populates="users")


class UserToken(Base):
    __tablename__ = "user_tokens"

    id = Column(Integer, primary_key=True)
    token = Column(String, nullable=False)
    user_type = Column(Integer)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    about = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # users = relationship(
    #     "User",
    #     secondary=association_table,
    #     back_populates="categories")
