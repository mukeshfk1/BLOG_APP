from sqlalchemy import Integer,String,Column,DateTime,ForeignKey,Text,select,func

from sqlalchemy.orm import relationship, column_property

from database import base

from flask_login import UserMixin


class User(base,UserMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key = True)
    name = Column(String(20))
    username = Column(String(25), unique = True,index = True)
    email = Column(String(30), unique = True ,index = True)
    password = Column(String(30))
    created_at = Column(DateTime)
    gender = Column(String(10))

    blog_user = relationship('Blogs',back_populates = "user_blog")

class Likes(base):
    __tablename__ = "likes"

    id = Column(Integer,primary_key = True)
    blog_id = Column(Integer,ForeignKey('blogs.id'))
    user_id = Column(Integer,ForeignKey(User.id))
    created_at = Column(DateTime)


class Blogs(base):
    __tablename__ = "blogs"

    id = Column(Integer,primary_key = True)
    title = Column(String(40))
    author = Column(Integer,ForeignKey(User.id))
    content = Column(Text)
    created_at = Column(DateTime)
    is_deleted = Column(Integer)

    user_blog = relationship('User',back_populates = "blog_user")
    
    like_count = column_property(select([func.count(Likes.id)]).where (Likes.blog_id == id))


    
