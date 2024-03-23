import kanu
import pymysql
import pymysql.cursors

class Database:
    def __init__(self):
        host = kanu.config.host
        user = kanu.config.user
        password = kanu.config.password
        db = kanu.config.db
        
        self.connection = pymysql.connect(
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

def setup():
    pass