import discord
from discord.ext import commands
import re
from os import system
from random import randint
from colorama import Fore, init
import json
import datetime
import time
import random, string
import os
import requests
from art import *
import asyncio
import base64

vert = "\033[32m"
blanc = "\033[37m"

with open('config.json', 'rt') as readfile:
    readconfig = json.load(readfile)

try:
    with open('config.json', 'rt') as readfile:
        readconfig = json.load(readfile)
except json.JSONDecodeError:
    print("Error: The JSON file is empty or has invalid content.")
    readconfig = {}
token = readconfig["token"]
prefix = readconfig["prefix"]
bot = commands.Bot(prefix, self_bot=True)
bot.remove_command('help')


banner = rf"""{vert}
  ___      _  __ _         _     _              _         _ _   
 / __| ___| |/ _| |__  ___| |_  | |__ _  _   __| |_____ _(_) |__
 \__ \/ -_) |  _| '_ \/ _ \  _| | '_ \ || | / _` / _ \ V / | / /
 |___/\___|_|_| |_.__/\___/\__| |_.__/\_, | \__,_\___/\_/|_|_\_\
                                      |__/                      
                                                           {blanc} V1
"""

maintenant = datetime.datetime.now()


init(convert=True)
def tokenid(ID):
    token = base64.b64encode(ID.encode("Utf-8"))
    return token.decode("Utf-8") 

def log(arg):
    annee = maintenant.year
    mois = maintenant.month
    jour = maintenant.day
    heure = maintenant.hour
    minute = maintenant.minute
    seconde = maintenant.second
    print(f"[{jour}/{mois}/{annee}][{heure}:{minute}:{seconde}][info]: {arg}")


@bot.event
async def on_ready():
    print(f"{banner}")
    print(f"Logged in as {vert}""{0.user}".format(bot))
    print(blanc)
        
@bot.command()
async def ping(ctx):
    await ctx.message.delete()
    before = time.monotonic()
    message = await ctx.send("Pong!")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"Pong!  `{int(ping)}ms`")
    ping2 = (f"Le ping du bot est de : {int(ping)}ms")
    log(ping2)

@bot.command()
async def gennitro(ctx):
    await ctx.message.delete()
    code = "https://discord.gift/" + ('').join(random.choices(string.ascii_letters + string.digits, k=16))
    await ctx.send(code)
    code2 = (f"Nitro générer : {code}")
    log(code2)
    
@bot.command()
async def clear(ctx, amount=5):
    logchannel = (f"Dans le salon {ctx.channel} il y a u {amount} message suprimer")
    await ctx.channel.purge(limit=amount + 1)
    log(logchannel)
    
@bot.command()
async def art(ctx, *, art=""):
    if art == "":
        await ctx.send("vous avez pas répondu !")
        return
    await ctx.message.delete()
    Art = text2art(art, "tarty1")
    await ctx.send(f"```{Art}```")
    

@bot.command(pass_context=True)
async def help(ctx, option=""):
    if option == "art":
        await ctx.send("```- !art <text> permet de faire de l'ascii art de façon automatique. Exemple : !art test```")
    elif option == "clear":
        await ctx.send("```- !clear <nombre> permet de supprimer le nombre de messages que l'on veut dans un serveur avec les droits. Exemple : !clear 20```")
    elif option == "gennitro":
        await ctx.send("```- !gennitro permet de générer un nitro aléatoire. Exemple : !gennitro```")
    elif option == "ping":
        await ctx.send("```- !ping permet de voir le nombre de pings du bot. Exemple : !ping```")
    else:
        await ctx.send("```- !ping : Test la latence du bot\n- !clear <nombre> : Supprime des messages (que sur un serveur avec les permissions)\n- !gennitro : Génère un nitro aléatoire\n- !art <text> : Affiche de l'ascii art\n Comming soon```")
        await ctx.send("```- !help <commande> : Pour avoir plus d'informations sur la commande\n Comming soon```")

bot.run(token, bot=False)