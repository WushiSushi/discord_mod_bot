import discord_conn
import sys
import json


def extract_json():
    file_ = open("settings.json")
    return json.load(file_)


def init():
    settings = extract_json()
    discord_conn.launch_discord_bot(settings["bot_token"])


if __name__ == "__main__":
    init()
