import discord
from discord.ext import commands

import sqlite3 as sqlite

class SQLRecorder:
    def __init__(self, filename:str):
        self.sqlite_file = sqlite.connect(filename)
        self.cursor = self.sqlite_file.cursor()
    
    def new_message(self, message:discord.Message):
