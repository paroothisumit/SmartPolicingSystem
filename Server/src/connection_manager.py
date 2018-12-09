import configparser

from mysql import connector


class DB:
    _db_connection = None
    _db_cur = None

    def __init__(self):
        db_config = configparser.ConfigParser()
        db_config.read('../mysql-properties.ini')
        print(type(dict(db_config['mysql_config'])))
        self._db_connection = connector.connect(**dict(db_config['mysql_config']))
        self._db_cur = self._db_connection.cursor(buffered=True)

    def query(self, query, params):
        self._db_cur.execute(query, params)
        print('Executed query:  ' + query + '   params:' + str(params))
        self._db_connection.commit()
        return self._db_cur

    def __del__(self):
        self._db_connection.close()


def __del__(self):
    self._db_connection.close()
