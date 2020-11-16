#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
import logging
from dotenv import load_dotenv
import discord
from discord.ext import commands
import modules

log = logging.getLogger("main")

def config_log():
    logging.basicConfig(
        format = '%(asctime)-30s %(name)-20s %(levelname)-10s %(message)s',
        level = logging.INFO,
    )

if __name__ == '__main__':
    load_dotenv()
    config_log()

    intents=discord.Intents.default()
    intents.members=True

    bot = commands.Bot(
        command_prefix=commands.when_mentioned_or("!"),
        description='Relatively simple music bot example',
        help_command=None,
        intents=intents
    )

    # Lista de módulos activa
    bot.add_cog(modules.WELCOME(bot))
    #bot.add_cog(modules.Music(bot))
    #bot.add_cog(modules.Other(bot))

    TOKEN = os.getenv("DISCORD_TOKEN")
    if TOKEN == None:
        log.info('Token not found ...')
        sys.exit(0)
    log.info('Bot started ...')

    bot.run(TOKEN)