import kanu
import pymysql
import pymysql.cursors
import time

class Database:
    def __init__(self):
        self.connection = self._wait_db()
        
    def _wait_db(self):
        while True:
            try:
                connection = pymysql.connect(
                    host=kanu.config.host,
                    user=kanu.config.user,
                    password=kanu.config.password,
                    database=kanu.config.database,
                    charset='utf8mb4',
                    autocommit=True,
                    cursorclass=pymysql.cursors.DictCursor)
                return connection
            except pymysql.err.OperationalError:
                time.sleep(1)

    def cursor(self) -> pymysql.cursors.DictCursor:
        return self.connection.cursor()
    
    def close(self):
        self.connection.close()
    
    def commit(self):
        self.connection.commit()

def setup():
    pass