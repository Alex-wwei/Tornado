
from sqlalchemy import text, Column, String, Integer, create_engine, CHAR, INT, ForeignKey, Index, TIMESTAMP, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

my_sql = create_engine("mysql+pymysql://root:qwe@127.0.0.1:3306/chouti_db?charset=utf8")
Base = declarative_base()
class User(Base):
    __tablename__ = 'user'

    uid = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(32))
    passwd = Column(String(32))
    mail = Column(String(32))
    ctime = Column(TIMESTAMP, nullable=False)

    __table_args__ = (
        Index('ix_user_pwd', 'username', 'passwd'),
        Index('ix_mail_pwd', mail, passwd),
    )

class News(Base):
    __tablename__ = 'news'

    nid = Column(Integer, autoincrement=True, primary_key=True)

    user_id = Column(Integer, ForeignKey("user.uid"))

    newstype_id = Column(Integer, ForeignKey("newstype.nid"))

    title = Column(String(128), nullable=False)
    url = Column(String(128), nullable=False)
    content = Column(String(200))

    ctime = Column(TIMESTAMP, nullable=False, server_default=text('NOW()'))
    fav_count = Column(Integer, nullable=False, default=0)
    # cmt_count = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return "{user_id:%s, 'newstype_id':%s, 'title':%s, 'url':%s, 'content':%s, 'ctime':%s}"%(self.user_id, self.newstype_id, self.title, self.url, self.content, self.ctime)

class NewsType(Base):
    __tablename__ = 'newstype'

    nid = Column(Integer, autoincrement=True, primary_key=True)
    types = Column(String(20), nullable=False)

class Favor(Base):
    __tablename__ = 'favor'

    fid = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.uid'))
    news_id = Column(Integer, ForeignKey('news.nid'))
    ctime = Column(TIMESTAMP, nullable=False)

    # __table_args__ = (
    __favor_args__ = (
        UniqueConstraint('user_id', 'news_id', 'uic_uid_nid'),
    )

class Conment(Base):
    __tablename__ = 'conment'

    cid = Column(Integer, autoincrement=True, primary_key=True)

    user_id = Column(Integer, ForeignKey('user.uid'))
    news_id = Column(Integer, ForeignKey('news.nid'))
    rpl_user_id = Column(Integer, ForeignKey('user.uid'))

    up = Column(Integer)
    down = Column(Integer)
    device = Column(String(32))
    comt = Column(String(120))

    ctime = Column(TIMESTAMP, nullable=False)

def drop_alltable():
    Base.metadata.drop_all(my_sql)#删除所有表结果
def create_alltable():
    Base.metadata.create_all(my_sql)#创建所有表结构

def session():
    return  sessionmaker(bind=my_sql)()

if __name__ == '__main__':

    # drop_alltable()
    create_alltable()

    sn = session()
    sn.add_all([
        NewsType(types = '42区'),
        NewsType(types='段子'),
        NewsType(types='图片'),
        NewsType(types='挨踢1024'),
        NewsType(types='你问我答'),
    ])
    sn.commit()#操作数据必须提交，放在命令后

