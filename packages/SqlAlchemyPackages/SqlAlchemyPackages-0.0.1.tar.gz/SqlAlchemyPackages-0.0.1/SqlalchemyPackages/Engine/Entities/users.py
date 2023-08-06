from sqlalchemy import Column, Integer, String

from SqlalchemyPackages.Engine import Base


class User(Base):
    # 指定本类映射到users表
    __tablename__ = 'users'

    # 指定id映射到id字段; id字段为整型，为主键
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    fullname = Column(String(32))
    password = Column(String(32))

    def __repr__(self):
        return "{'id'='%s','name'='%s', 'fullname'='%s', 'password'='%s'}" % (self.id, self.name, self.fullname, self.password)
