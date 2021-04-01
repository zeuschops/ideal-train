import requests
import discord
from discord.ext import commands

class RiotGamesAPI(commands.Cog):
    def __init__(self, bot, token:str):
        self.bot = bot
        self.headers = {'X-Riot-Token': token}
        self.endpoints = {
            'na':'https://na1.api.riotgames.com',
            'euw':'https://euw1.api.riotgames.com',
            'eun':'https://eun1.api.riotgames.com',
            'br':'https://br1.api.riotgames.com',
            'jp':'https://jp1.api.riotgames.com',
            'kr':'https://kr.api.riotgames.com',
            'la1':'https://la1.api.riotgames.com',
            'la2':'https://la2.api.riotgames.com',
            'oc':'https://oc1.api.riotgames.com',
            'tr':'https://tr1.api.riotgames.com',
            'ru':'https://ru.api.riotgames.com',
            'americas':'https://americas.api.riotgames.com',
            'asia':'https://asia.api.riotgames.com',
            'europe':'https://europe.api.riotgames.com'
        }
    
    @commands.command()
    async def summoner(self, ctx, region:str, summoner:str):
        resp = requests.get(self.endpoints[region.lower()] + '/lol/summoner/v4/summoners/by-name/' + summoner, headers=self.headers)
        if resp.status_code == 200:
            resp_j = resp.json()
            embed = discord.Embed(title=resp_j['name'], url='https://matchhistory.na.leagueoflegends.com/en/#match-history/NA1/230089557')
            embed.add_field(name='id', value=resp_j['id'])
            embed.add_field(name='accountId', value=resp_j['accountId'])
            embed.add_field(name='puuid', value=resp_j['puuid'])
            embed.add_field(name='revisionDate', value=resp_j['revisionDate'])
            embed.add_field(name='summonerLevel', value=resp_j['summonerLevel'])
            embed.set_thumbnail(url='http://ddragon.leagueoflegends.com/cdn/11.7.1/img/profileicon/' + str(resp_j['profileIconId']) + '.png')
            await ctx.send(embed=embed)
    
    @commands.command()
    async def riotregions(self, ctx):
        await ctx.send('Available regions are ' + str(list(self.endpoints)))
