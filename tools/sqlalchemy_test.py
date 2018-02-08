# Created by Max on 2/8/18
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(String(20), primary_key=True)
    name = Column(String(20))


# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/springdemo')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

session = DBSession()
new_user = User(id='2', name='Rule')
session.add(new_user)
session.commit()
session.close()
