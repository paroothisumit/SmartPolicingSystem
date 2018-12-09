from mysql import connector


class DB:
    _db_connection = None
    _db_cur = None

    def __init__(self):

        self._db_connection = connector.connect(user='root',db='serverdb',password='sumit2000',auth_plugin='mysql_native_password')
        self._db_cur = self._db_connection.cursor(buffered=True)

    def query(self, query, params):

        self._db_cur.execute(query, params)
        print('Executed query:  '+query+'   params:'+str(params))
        self._db_connection.commit()
        return self._db_cur
    def __del__(self):
        self._db_connection.close()



def __del__(self):
    self._db_connection.close()
