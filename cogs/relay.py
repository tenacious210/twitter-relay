import time
import json
from discord import app_commands
from discord.ext import tasks, commands
from bs4 import BeautifulSoup
from selenium import webdriver
from threading import Thread

## all reading and writing of files should now be handled with the helpers.config module
from helpers.config import logging, read_channels, write_channels

logger = logging.getLogger(__name__)


class Relay(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.channels = read_channels()
        Thread(target=self.parsing).start()

    @commands.command()
    async def init(self, ctx):
        if ctx.channel.id not in self.channels:
            self.channels.append(ctx.channel.id)
        write_channels(self.channels)
        await ctx.send()

    def parsing(self):
        # Destiny Collections
        data = {}
        parsed_data = []

        driver = webdriver.Chrome()

        # Driver Manipulation
        driver.get("https://nitter.moomoo.me/mrbeast")
        respose = driver.page_source
        driver.close()

        # Parsing...
        soup = BeautifulSoup(respose, "html.parser")

        # Profile Name and Handle
        name_handle = soup.find("div", {"class": "profile-card-tabs-name"})
        try:
            data["profile_name"] = name_handle.find(
                "a", {"class": "profile-card-fullname"}
            ).text
        except:
            data["profile_name"] = None
        try:
            data["profile_handle"] = name_handle.find(
                "a", {"class": "profile-card-username"}
            ).text
        except:
            data["profile_handle"] = None

        # Following and Follower Count
        following_followers = soup.find("div", {"class": "profile-card-extra-links"})
        try:
            data["profile_following"] = (
                following_followers.find("li", {"class": "following"})
                .find("span", {"class": "profile-stat-num"})
                .text
            )
        except:
            data["profile_following"] = None
        try:
            data["profile_followers"] = (
                following_followers.find("li", {"class": "followers"})
                .find("span", {"class": "profile-stat-num"})
                .text
            )
        except:
            data["profile_followers"] = None

        # Most Recent Tweet
        tweet = soup.find("div", {"class": "tweet-body"})
        try:
            data["most_recent_tweet"] = tweet.find(
                "div", {"class", "tweet-content media-body"}
            ).text
        except:
            data["most_recent_tweet"] = None

        # Data Manipulation
        parsed_data.append(data)

        relayed_name = ""
        relayed_handle = ""
        relayed_following = ""
        relayed_followers = ""
        relayed_tweet = ""

        for items in parsed_data:
            for item in items:
                relayed_name = items["profile_name"]
                relayed_handle = items["profile_handle"]
                relayed_following = items["profile_following"]
                relayed_followers = items["profile_followers"]
                relayed_tweet = items["most_recent_tweet"]

        for ids in self.channels:
            channel = self.client.get_channel(ids)
            self.client.loop.create_task(
                channel.send(f"{relayed_name} ({relayed_handle}): {relayed_tweet}")
            )

        time.sleep(10.0)


async def setup(client):
    await client.add_cog(Relay(client))
