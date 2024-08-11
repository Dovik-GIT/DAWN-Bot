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
import nmap
import subprocess

vert = "\033[32m"
blanc = "\033[37m"
rouge = "\033[31m"

nm = nmap.PortScanner()


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
nitrosnip = readconfig["nitrosnip"]

bot = commands.Bot(prefix, self_bot=True)
bot.remove_command('help')

if nitrosnip == "False":
    couleursnip = rouge
elif nitrosnip == "True":
    couleursnip = vert
else:
    couleursnip = rouge


banner = rf"""{vert}
  ___      _  __ _         _     _              _         _ _   
 / __| ___| |/ _| |__  ___| |_  | |__ _  _   __| |_____ _(_) |__
 \__ \/ -_) |  _| '_ \/ _ \  _| | '_ \ || | / _` / _ \ V / | / /
 |___/\___|_|_| |_.__/\___/\__| |_.__/\_, | \__,_\___/\_/|_|_\_\
                                      |__/                      
    {blanc} Nitro Snip : {couleursnip}{nitrosnip}                      {blanc} V2
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

def restart():
    os.execv(sys.executable, ['python'] + sys.argv)


def checktoken():
    headers = {
        'Authorization': f'{token}'
    }
    url = 'https://discord.com/api/v9/users/@me'
    response = requests.get(url, headers=headers)
    try:
        response.raise_for_status()
        print(f"{vert}Valid Token{blanc}")
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
async def on_message(message):
    if message.content == "":
        return
    log(f"{message.author} | {message.content}")
    if "https://discord.gift/" in message.content:
        #chepa la syntax
        if nitrosnip == "False":
            return
        elif nitrosnip == "True":
            pattern = r'https://discord\.gift/[^\s]+'
            liens = re.findall(pattern, message.content)
            pattern = r'https://discord\.gift/([a-zA-Z0-9]+)'
            match = re.search(pattern, message.content)
            identifiant = match.group(1)
            for lien in liens:

                url = f"https://discord.com/api/v9/entitlements/gift-codes/{identifiant}?country_code=FR&with_application=true&with_subscription_plan=true"

                headers = {
                    'Referer': f'{lien}',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.124 Safari/537.36',
                    'Authorization': f'{token}'
                }

                response = requests.get(url, headers=headers)
                reponsenitro = response["code"]
                if reponsenitro == "10038":
                    print("Invalid nitro")
        else:
            return
    if message.content.lower() == 'truc':
        if message.author == bot.user:
            return
        await message.channel.send(f'Salut {message.author} !')

    await bot.process_commands(message)
@bot.event
async def on_ready():
    print(f"{banner}")
    print(f"Logged in as {vert}""{0.user}".format(bot))
    print(blanc)
        


@bot.command()
async def sniper(ctx, truc):
    if truc == "True":
        readconfig["nitrosnip"] = truc
        with open('config.json', 'w') as file:
            json.dump(readconfig, file, indent=4)
        await ctx.send(f"```Config changer {truc}```")
        restart()
    elif truc == "False":
        readconfig["nitrosnip"] = truc
        with open('config.json', 'w') as file:
            json.dump(readconfig, file, indent=4)
        await ctx.send(f"```Config changer {truc}```")
        restart()
    else: 
        await ctx.send("```Invalid Option True or False```")
    

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
async def clear(ctx, *, number : int = 10):
    logchannel = (f"Dans le salon {ctx.channel} il y a u {number} message suprimer")
    async for msg in ctx.channel.history(limit= number + 1):
        if msg.author == bot.user:
            await msg.delete()
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

@bot.command()
async def kick(ctx, member: discord.user, *, reason=None):
    if ctx.guild is None:
        await ctx.send("Cette commande doit ètre exécuter dans un serveur")
        return
    try:
        await member.kick(reason=reason)
        await ctx.send(f"{member} a été exclu")
    except:
        await ctx.send(f"une erreur est survenue avez vous les droits ?")


def check_nmap_installed():
    try:
        result = subprocess.run(['nmap', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return True
        else:
            return False
    except FileNotFoundError:

        return False

@bot.command()
async def nmap(ctx, ip):
    nmapcheck = check_nmap_installed()
    if nmapcheck == False:
        await ctx.send("Merci d'installer nmap sur votre machine !")
        return
    result = subprocess.run(['nmap', ip], capture_output=True, text=True)
    output = result.stdout
    lignes = output.split('\n')
    listport = []
    for ligne in lignes:
        if ligne and ligne[0].isdigit():
            details = ligne.split()
            port = details[0]
            service = details[2]
            listport.append(f"Port: {port} | Service: {service}")

    # Construction du message avec une meilleure mise en forme
    portresult = '\n'.join(listport)
    formatted_message = (
        "```\n"
        "Résultats du scan Nmap\n"
        "====================\n\n"
        f"{portresult}\n"
        "```\n"
    )
    await ctx.send(formatted_message)

@bot.command()
async def mass_emoji(ctx, emoji: str, count: int):
    if count > 100:
        await ctx.send("Je ne peux ajouter des emojis qu'à 100 messages à la fois.")
        return

    messages = await ctx.channel.history(limit=count).flatten()

    for message in messages:
        try:
            await message.add_reaction(emoji)
        except discord.HTTPException:
            await ctx.send(f"Je n'ai pas pu ajouter l'emoji {emoji} à un message.")
        except discord.InvalidArgument:
            await ctx.send(f"L'emoji {emoji} n'est pas valide.")
        except discord.Forbidden:
            await ctx.send("Je n'ai pas les permissions pour ajouter des emojis à ces messages.")
            break

    msg = await ctx.send(f"{emoji} a été ajouté à {len(messages)} messages.")
    await msg.delete(delay=4)

@bot.command()
async def random_emojis(ctx):

    emojis = ["😀", "😁", "😂", "🤣", "😃", "😄", "😅", "😆", "😉", "😊", "😋", "😎", "😍", "🥰", "😘", "😗", "😙", "😚", "☺️", "🙂", "🤗", "🤩", "🤔", "🤨", "😐", "😑", "😶", "🙄", "😏", "😣", "😥", "😮", "🤐", "😯", "😪", "😫", "😴", "😌", "😛", "😜", "😝", "🤤", "😒", "😓", "😔", "😕", "🙃", "🤑", "😲", "☹️", "🙁", "😖", "🥵", "😞", "😟", "🥶", "🥴", "😤", "😢", "😭", "😦", "😧", "🥳", "😨", "😩", "🤯", "😬", "😰", "😱", "😳", "🤪", "😵", "😡", "🥺", "😠", "🤬", "😷", "🤒", "🤕", "🤢", "🤮", "🤧", "😇", "🤠", "🤥", "🤫", "🤭", "🧐", "🤓", "😈", "👿", "🤡", "👹", "👺", "💀", "☠️", "👻", "👽", "👾", "🤖", "💩", "🙊"]
    messages = await ctx.channel.history(limit=5).flatten()
    for message in messages:
        random_emoji = random.choice(emojis)
        try:
            await message.add_reaction(random_emoji)
            random_emoji = random.choice(emojis)
            await message.add_reaction(random_emoji)
            random_emoji = random.choice(emojis)
            await message.add_reaction(random_emoji)
            random_emoji = random.choice(emojis)
            await message.add_reaction(random_emoji)
            random_emoji = random.choice(emojis)
            await message.add_reaction(random_emoji)
            
        except discord.HTTPException:
            await ctx.send(f"Je n'ai pas pu ajouter l'emoji {random_emoji} à un message.")
        except discord.Forbidden:
            await ctx.send("Je n'ai pas les permissions pour ajouter des emojis à ces messages.")
            break


@bot.command()
async def help(ctx, option=""):
    if option == "art":
        await ctx.send(f"```markdown\n- {ctx.prefix}art <text> : Permet de faire de l'ASCII art de façon automatique. Exemple : {ctx.prefix}art test```")
    elif option == "sniper":
        await ctx.send(f"```markdown\n- {ctx.prefix}sniper <True/False> : Permet de lancer ou d'arrêter le nitro sniper. Exemple : {ctx.prefix}sniper False```")
    elif option == "clear":
        await ctx.send(f"```markdown\n- {ctx.prefix}clear <nombre> : Permet de supprimer le nombre de messages souhaité dans un serveur avec les droits nécessaires. Exemple : {ctx.prefix}clear 20```")
    elif option == "gennitro":
        await ctx.send(f"```markdown\n- {ctx.prefix}gennitro : Génère un nitro aléatoire. Exemple : {ctx.prefix}gennitro```")
    elif option == "ping":
        await ctx.send(f"```markdown\n- {ctx.prefix}ping : Teste la latence du bot. Exemple : {ctx.prefix}ping```")
    elif option == "ipinfo":
        await ctx.send(f"```markdown\n- {ctx.prefix}ipinfo <ip> : Récupère toutes les informations de l'adresse IP et les envoie en JSON. Exemple : {ctx.prefix}ipinfo 8.8.8.8```")
    elif option == "kick":
        await ctx.send(f"```markdown\n- {ctx.prefix}kick <membre> [raison] : Exclut un membre du serveur. Exemple : {ctx.prefix}kick @membre raison```")
    elif option == "nmap":
        await ctx.send(f"```markdown\n- {ctx.prefix}nmap <ip> : Effectue un scan nmap sur l'adresse IP spécifiée. Exemple : {ctx.prefix}nmap 8.8.8.8```")
    elif option == "mass_emoji":
        await ctx.send(f"```markdown\n- {ctx.prefix}mass_emoji <emoji> <nombre> : Ajoute l'emoji spécifié aux derniers messages du canal (max 100 messages). Exemple : {ctx.prefix}mass_emoji 😀 20```")
    elif option == "random_emojis":
        await ctx.send(f"```markdown\n- {ctx.prefix}random_emojis : Ajoute des emojis aléatoires aux derniers messages du canal (jusqu'à 5 emojis par message).```")
    else:
        await ctx.send(f"```markdown\n#Selfbot By Dovik\n- {ctx.prefix}ipinfo <ip> : Permet de récupérer les informations de l'adresse IP\n- {ctx.prefix}ping : Teste la latence du bot\n- {ctx.prefix}clear <nombre> : Supprime des messages (que sur un serveur avec les permissions)\n- {ctx.prefix}gennitro : Génère un nitro aléatoire\n- {ctx.prefix}art <text> : Affiche de l'ASCII art\n- {ctx.prefix}sniper <True/False> : Active ou désactive le nitro sniper\n- {ctx.prefix}kick <membre> [raison] : Exclut un membre du serveur\n- {ctx.prefix}nmap <ip> : Effectue un scan nmap sur l'adresse IP\n- {ctx.prefix}mass_emoji <emoji> <nombre> : Ajoute un emoji aux derniers messages du canal\n- {ctx.prefix}random_emojis : Ajoute des emojis aléatoires aux derniers messages du canal```")
        await ctx.send(f"```markdown\n- {ctx.prefix}help <commande> : Pour obtenir plus d'informations sur une commande spécifique```")

bot.run(token, bot=False)