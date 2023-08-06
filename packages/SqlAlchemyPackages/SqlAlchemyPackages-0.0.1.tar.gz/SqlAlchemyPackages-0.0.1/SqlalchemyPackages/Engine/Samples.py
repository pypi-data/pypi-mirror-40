from SqlalchemyPackages.Engine import Session
from SqlalchemyPackages.Engine.Entities import User
from SqlalchemyPackages.Engine.Devices import create_all

create_all()


def sample_add(**kwargs):
    ed_user = User(name=kwargs['name'], fullname=kwargs['fullname'], password=kwargs['password'])
    Session.add(ed_user)
    Session.commit()


def sample_add_all():
    Session.add_all([
        User(name='A', fullname='Ed Jones', password='edspassword'),
        User(name='B', fullname='Ed Jones', password='edspassword'),
        User(name='C', fullname='Ed Jones', password='edspassword')
    ])
    Session.commit()


def sample_query_all(**kwargs):
    """
    建议使用filter_by
    :return:
    """
    our_user = Session.query(User).filter_by(name=kwargs["name"]).all()
    for user in our_user:
        print(user)


def sample_query_first():
    """
    带参数需要使用filter替代filter_by
    :return:
    """
    table_and_column_name = User
    filter = (User.name == 'A')
    our_user = Session.query(table_and_column_name).filter(filter).first()
    print(our_user)


def sample_modify(**kwargs):
    mod_user = Session.query(User).filter_by(name=kwargs["name"]).all()
    for user in mod_user:
        user.password = 'modify_passwd'
    Session.commit()


def sample_delete(**kwargs):
    del_user = Session.query(User).filter_by(name=kwargs['name']).all()
    for user in del_user:
        Session.delete(user)
    Session.commit()


if __name__ == "__main__":
    print("添加")
    sample_add(name='wyd', password='password', fullname='weiyingda')
    print("查询")
    sample_query_all(name='wyd')
    print("修改")
    sample_modify(name='wyd')
    print("查询")
    sample_query_all(name='wyd')
    print("删除")
    sample_delete(name='wyd')
    print("查询")
    sample_query_all(name='wyd')
