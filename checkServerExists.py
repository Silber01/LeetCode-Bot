import os
import json
from os.path import exists

def checkServerExists(ctx):
    serverID = str(ctx.guild.id)
    if not exists(f"./servers/{serverID}.json"):
        with open("./initFiles/server.json", "r") as readFile: 
            server = json.load(readFile)
        with open(f"./servers/{serverID}.json", "w") as writeFile:
            json.dump(server, writeFile)
