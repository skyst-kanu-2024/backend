import kanu
import pymysql
import pymysql.cursors

class Database:
    def __init__(self):
        host = kanu.config['database']['host']
        user = kanu.config['database']['user']
        password = kanu.config['database']['password']
        db = kanu.config['database']['db']
        
        self.connection = pymysql.connect(host=host,
            host=host,
            user=user,
            password=password,
            db=db,
            charset='utf8mb4',
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor)

    def cursor(self) -> pymysql.cursors.DictCursor:
        return self.connection.cursor()
    
    def close(self):
        self.connection.close()
    
    def commit(self):
        self.connection.commit()
    