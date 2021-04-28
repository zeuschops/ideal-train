import discord
from discord.ext import commands

import sqlite3 as sqlite
import datetime

class SQLRecorder:
    def __init__(self, filename:str):
        self.sqlite_file = sqlite.connect(filename)
        self.cursor = self.sqlite_file.cursor()

    def new_message(self, message:discord.Message):
        print("New Message")
        print("\tID:", message.id)
        print("\tAuthor ID:", message.author.id)
        print("\tTimestamp:", message.timestamp.strftime("%Y-%m-%d %H:%M:%S"))
    
    def edit_message(self, message:discord.Message):
        print("Edit Message")
        print("\tID:", message.id)
        print("\tAuthor ID:", message.author.id)
        print("\tTimestamp:", message.timestamp.strftime("%Y-%m-%d %H:%M:%S"))
    
    def deleted_message(self, message:discord.Message):
        print("Message deleted")
        print("\tID:", message.id)
        print("\tAuthor ID:", message.author.id)
        print("\tDeleted at:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    def joined_voice(self, member:discord.Member, channel:discord.VoiceChannel):
        print("Member joined voice")
        print("\tMember ID:", member.id)
        print("\tChannel ID:", channel.id)
        print("\tGuild ID:", channel.guild.id)
    
    def left_voice(self, member:discord.Member, channel:discord.VoiceChannel):
        print("Member left voice")
        print("\tMember ID:", member.id)
        print("\tChannel ID:", channel.id)
        print("\tGuild ID:", channel.guild.id)
    
    def get_user(self, id:str):
        self.cursor.execute("SELECT * FROM users WHERE id=\"%s\"" % id)
        return self.cursor.fetchall()
    
    def member_joined(self, member:discord.Member):
        print("Member joined Guild")
        print("\tMember ID:", member.id)
        print("\tGuild ID:", member.guild.id)
        print("\tTimestamp:", member.joined_at.strftime('%Y-%m-%d %H:%M:%S'))
    
    def member_left(self, member:discord.Member):
        print("Member lefted Guild")
        print("\tMember ID:", member.id)
        print("\tGuild ID:", member.guild.id)
        print("\tTimestamp:", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def other(self, sql_query:str, fetchall:bool, commit:bool):
        self.cursor.execute(sql_query)
        if fetchall and not commit:
            return self.cursor.fetchall()
        if commit:
            self.sqlite_file.commit()
            return []
