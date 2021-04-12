import sqlite3 as sqlite

class SQLRecorder:
    def __init__(self, filename:str):
        self.sqlite_file = sqlite.connect(filename)
        self.cursor = self.sqlite_file.cursor()
    
    def create_message_table(self):
        