
from  .database   import Base
from sqlalchemy.sql.expression import null
from sqlalchemy import Column,String,Boolean,Integer,text,ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP 
from sqlalchemy.orm import relationship


class Posts(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(String(1000), nullable=False)
    published = Column(Boolean, server_default=text("False"),nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), nullable=False)

    owner = relationship("Users")

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(255), nullable=False,unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"), primary_key=True)
