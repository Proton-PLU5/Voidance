import discord
from discord.ext import commands
import os
from github import Github
import pygit2
import time
import AutoFetch
import calendar
import requests
import json

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

# Variables
home = os.getcwd()
git = None
repository = None
# Globals
console_id = 831818499730440212
announcement_id = 0
latestRelease = ""
previousRelease = ""
newRelease = ""
url = ""

REPO_OWNER = "Proton-PLU5"
REPO_NAME = "Voidance"
USERNAME = "ProDarkNinja"
PASSWORD = "ProDarkNinja3"


def make_github_issue(title, body=None, labels=None):
    

@client.event
async def on_ready():
    global git
    global console_id
    global announcement_id
    global repository
    global previousRelease
    global latestRelease
    # Getting Github API
    try:
        git = Github("ProDarkNinja", "ProDarkNinja3")
        repository = git.get_repo("Proton-PLU5/Voidance")
        repository.create_issue()

    except Exception as e:
        print("API Exception Config")
    # Getting all variables from config
    previousRelease = repository.get_latest_release()
    latestRelease = repository.get_latest_release()
    print(client.user.name + " has connected!")


@client.event
async def on_message(message):
    global console_id
    global newRelease
    if message.author.name != client.user.name:
        if message.content.startswith("git!"):
            print("Command Executing?")

            if 'getReleases' in message.content:
                await getReleases(message)
            elif 'Test' in message.content:
                await Test(message)
            elif 'issue' in message.content:
                title = ''
                body = ''
                newstring = message.content.replace("git!issue ", "")
                for letters in newstring:
                    if (' ' not in letters):
                        title = title + letters
                    else:
                        break
                newstring = newstring.replace(title + " ", "")
                for letters in newstring:
                    body = body + letters

                make_github_issue(title=title, body=body)
                print("Made Issue!")
        else:
            pass
            await autoFetch()
            await GetUsers()


async def getReleases(ctx):
    global git
    global repository
    global latestRelease
    try:
        repository = git.get_repo("Proton-PLU5/Voidance")
        releases = repository.get_releases()
        titles = []
        await ctx.channel.send("Getting latest releases:")
        for i in releases:
            titles.append(i.title)
            await ctx.channel.send(i.title)

        size = len(titles)
        latestRelease = releases[size - 1]
        await ctx.channel.send("Saved Latest Release!")
    except Exception as e:

        await ctx.channel.send("Couldn't Get Releases, API Exception!")


async def Test(ctx):
    await ctx.channel.send("Test")
    print("Test!")


async def autoFetch():
    global newRelease
    global previousRelease
    global url
    newRelease, previousRelease = AutoFetch.AutoFetch(previousRelease=previousRelease)
    if newRelease == "":
        print("API Exception Fetching")
        print("Skipped Fetch!")
        return
    else:
        if console_id != 0:
            print("Console id is not 0")
            channel = client.get_channel(console_id)
            if newRelease is not None:
                await channel.send("New Release! " + newRelease.title)
                url = repository.get_latest_release().zipball_url
                await channel.send("Download URL: " + str(url))
                newRelease = ""

    print("Fetched")
    print(newRelease.title)


async def GetUsers():
    global url
    users = client.get_all_members()
    data = []
    os.chdir(os.getcwd() + "/data")
    with open("data.txt", "r") as f:
        data = f.readlines()
    for user in users:
        for i in range(0, len(data)):
            if user.name != data[i]:
                embed = discord.Embed(title="New Voidance Mods!", description="There has been new mods added to "
                                                                              "Voidance. The mods are found in the "
                                                                              "voidance github, I have created a "
                                                                              "special download link for you to "
                                                                              "use!\n\n "
                                                                              "This is a message that is "
                                                                              "sent automatically when a new Voidance "
                                                                              "mod update is made.\n If you don't want "
                                                                              "to get updates anymore DM Proton+.\n "
                                                                              "Get them now using the url underneath! "
                                                                              "Copyright ProtonPLUS\n\nInstall "
                                                                              "Instructions:\n1. Download the zip "
                                                                              "file and right click it and press "
                                                                              "extract.\n2. Go inside the new folder "
                                                                              "and into mods, click and drag to "
                                                                              "select all the mods. Then right click "
                                                                              "and copy.\n3. Press Windows Key + R "
                                                                              "and type %appdata% and press OK "
                                                                              "button.\n4. Go into .minecraft folder "
                                                                              "and then into mods.\n5. Delete "
                                                                              "everything there, And paste the copied "
                                                                              "mods.\n If you need assistance contact "
                                                                              "ProtonPLUS or TypicalZedF \nThese Mods "
                                                                              "are "
                                                                              "valid from " + str(
                    calendar.datetime.datetime.today().strftime('%Y-%m-%d')), color=discord.Color.purple(), url=url, )
                await DMUser(user, embed, url)
                print(url)


async def DMUser(user, message, Url):
    channel = await user.create_dm()
    await channel.send_message(embed=message)
    await channel.send_message("Download URL: " + Url)
    await channel.send_message("👌")
    # await discord.DMChannel.send(user, embed=message)
    # await discord.DMChannel.send(user, "Download URL: " + Url)
    # await discord.DMChannel.send("👌")


client.run("ODMxODEwNTYyMTUyMjAyMjcx.YHap9A.OFKCE_XsXwQOIbPAyHxYfBrHiGk")
