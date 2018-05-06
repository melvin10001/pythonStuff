import sqlite3 as lite


class ConnectionError(Exception):
    pass

class CredentialError(Exception):
    pass

class SQLError(Exception):
    pass

class UseDatabase:
    
    def __init__(self,database_name:int) -> None:
        self.database_name = database_name
    
    def __enter__(self) -> 'cursor':
        try:
            self.connection = lite.connect(self.database_name)
            self.cursor = self.connection.cursor()
            return self.cursor
        except lite.InterfaceError as err:
            raise ConnectionError(err)
        except lite.ProgrammingError as err:
            raise CredentialError(err)

    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        if exc_type is lite.ProgrammingError:
            raise SQLError(exc_value)

