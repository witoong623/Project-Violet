import pymysql

def get_database():
    ''' return connection instance that was setup to local mysql '''
    db = pymysql.connect(host='localhost',
                           user='root',
                           password='123456',
                           db='football_recommend',
                           charset='utf8mb4')
    return db