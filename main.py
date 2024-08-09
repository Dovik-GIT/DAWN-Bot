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
import sys


vert = "\033[32m"
blanc = "\033[37m"
rouge = "\033[31m"


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

def clearconsol():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def progress_bar(iteration, total, length=50):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r|{bar}| {percent}%')
    sys.stdout.flush()



def checktoken():
    headers = {
        'Authorization': f'{token}'
    }
    url = 'https://discord.com/api/v9/users/@me'
    response = requests.get(url, headers=headers)
    try:
        response.raise_for_status()
        print(f"{vert}Valid Token{blanc}")
        total = 100
        for i in range(total + 1):
            progress_bar(i, total)
            time.sleep(0.02)
        clearconsol()
    except:
        print(f"{rouge}Invalide Token{blanc}")
        time.sleep(3)
        exit(1)

checktoken()

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
    

@bot.command()
async def ipinfo(ctx, ipaddress: str):

    url = f"http://ip-api.com/json/{ipaddress}"

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0 (Edition std-2)',
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    if data['status'] == 'fail':
        await ctx.send(f"Erreur lors de la récupération des informations pour l'adresse IP {ipaddress}.")
        return
    
    #{'status': 'success', 'country': 'United States', 'countryCode': 'US', 'region': 'VA', 'regionName': 'Virginia', 'city': 'Ashburn', 'zip': '20149', 'lat': 39.03, 'lon': -77.5, 'timezone': 'America/New_York', 'isp': 'Google LLC', 'org': 'Google Public DNS', 'as': 'AS15169 Google LLC', 'query': '8.8.8.8'}
    
    #contry = data["country"]
    #status = data["status"]
    #countryCode = data["countryCode"]
    #region = data["region"]
    #regionName = data["regionName"]
    #city = data["city"]
    #zip_code = data["zip"]
    #lat = data["lat"]
    #lon = data["lon"]
    #timezone = data["timezone"]
    #isp = data["isp"]
    #org = data["org"]
    #as_info = data["as"]
    #query = data["query"]
    
    await ctx.send(f"```{data}```")


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
    elif option == "ipinfo":
        await ctx.send("```- !ipinfo <commande> Récupère toute les informations de l'adresse ip et l'envoie en json. Exemple : !ipinfo 8.8.8.8```")
    else:
        await ctx.send("```- !ipinfo <ip> Permet de récupérer les informations de l'adresse ip\n- !ping : Test la latence du bot\n- !clear <nombre> : Supprime des messages (que sur un serveur avec les permissions)\n- !gennitro : Génère un nitro aléatoire\n- !art <text> : Affiche de l'ascii art\n Comming soon```")
        await ctx.send("```- !help <commande> : Pour avoir plus d'informations sur la commande\n Comming soon```")

bot.run(token, bot=False)