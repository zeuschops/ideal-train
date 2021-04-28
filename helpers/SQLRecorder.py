import discord
from discord.ext import commands

import sqlite3 as sqlite
import datetime

class SQLRecorder:
    def __init__(self, filename:str):
        self.sqlite_file = sqlite.connect(filename)
        self.cursor = self.sqlite_file.cursor()

    def initialize(self):
        self.cursor.execute("CREATE TABLE message(id text not null,"
                            + "author_id text not null,"
                            + "channel_id text not null,"
                            + "guild_id text not null,"
                            + "content text,"
                            + "timestamp DATETIME not null default now()"
                            + ");")
        self.cursor.execute("CREATE TABLE member(id text not null, "
                            + "name text not null, "
                            + "discriminator int not null, "
                            + "guild text not null"
                            + ");")
        self.cursor.execute("CREATE TABLE guild(id text not null, "
                            + "name text not null, "
                            + "owner_id text not null"
                            + ");")
        self.cursor.execute("CREATE TABLE activity(id int autoincrement, "
                            + "activity_id int not null, "
                            + "reference_id text not null,"
                            + "timestamp DATETIME default now()"
                            + ");")
        self.cursor.execute("CREATE TABLE activity_ids(id int autoincrement, "
                            + "name text not null);")
        #Add some default values for activity_ids for lookup later...
        self.cursor.execute("INSERT INTO activity_ids(name) VALUES (\"joined_voice\"),(\"left_voice\"),(\"new_message\"),(\"edited_message\"),(\"deleted_message\"),(\"joined_guild\"),(\"left_guild\"),(\"member_joined_guild\"),(\"member_left_guild\");")
        self.sqlite_file.commit()

    def add_message(self, message:discord.Message, new_message:bool):
        self.cursor.execute("INSERT INTO message(id, author_id, channel_id, guild_id, content, timestamp) VALUES (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\")" % (messaage.id, message.author.id, message.channel.id, message.guild.id, message.content, message.created_at.strftime("%Y-%m-%d %H:%M:%S")))
        self.sqlite_file.commit()

    def new_message(self, message:discord.Message):
        print("New Message")
        print("\tID:", message.id)
        print("\tAuthor ID:", message.author.id)
        print("\tTimestamp:", message.timestamp.strftime("%Y-%m-%d %H:%M:%S"))
        self.add_message(message, True)
        
    def edit_message(self, message:discord.Message):
        print("Edit Message")
        print("\tID:", message.id)
        print("\tAuthor ID:", message.author.id)
        print("\tTimestamp:", message.timestamp.strftime("%Y-%m-%d %H:%M:%S"))
        self.add_message(message, False)
    
    def deleted_message(self, message:discord.Message):
        print("Message deleted")
        print("\tID:", message.id)
        print("\tAuthor ID:", message.author.id)
        print("\tDeleted at:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.cursor.execute("INSERT INTO activity(activity_id, reference_id) VALUES (4, \"%s\")" % message.id)
    
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
