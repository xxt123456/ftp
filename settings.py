from  DBUtils.PooledDB import PooledDB,SharedDBConnection
import pymysql
class Config(object):
    SALA=b'123'
    SECRET_KEY='asdsda'
    MAX_CONTENT_LENGTH=1024 * 1024 * 7

    POOL=PooledDB(
        creator=pymysql,
        maxconnections=5,
        mincached=2,
        maxcached=3,
        maxshared=3,
        blocking=True,
        maxusage=None,
        setsession=[],
        ping=0,
        host='127.0.0.1',
        port=3306,
        user='root',
        password='123456',
        database='codeftp',
        charset='utf8'
    )