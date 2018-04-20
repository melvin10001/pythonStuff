import sqlite3 as lite

class UseDatabase:
    
    def __init__(self,database_name:int) -> None:
        self.database_name = database_name
    
    def __enter__(self) -> 'cursor':
        self.connection = lite.connect(self.database_name)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

