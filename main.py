#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import logging
from dotenv import load_dotenv
import discord
from discord.ext import commands
import modules

def config_log():
    logging.basicConfig(
        format = '%(asctime)-30s %(name)-20s %(levelname)-10s %(message)s',
        level = logging.INFO,
    )

if __name__ == '__main__':
    load_dotenv()
    config_log()
    bot = commands.Bot(
        command_prefix=commands.when_mentioned_or("!"),
        description='Relatively simple music bot example'
    )

    # Lista de módulos activa
    bot.add_cog(modules.Music(bot))
    bot.add_cog(modules.Other(bot))

    TOKEN = os.getenv("DISCORD_TOKEN")
    logging.info('Bot started ...')
    bot.run(TOKEN)

