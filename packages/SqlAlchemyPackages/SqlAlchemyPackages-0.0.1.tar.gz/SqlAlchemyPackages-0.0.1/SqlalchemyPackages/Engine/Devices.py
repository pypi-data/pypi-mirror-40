from SqlalchemyPackages.Engine import engine, Base


def create_all():
    """
    创建数据表
    :return:
    """
    Base.metadata.create_all(engine)
