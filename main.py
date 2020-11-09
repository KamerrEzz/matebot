#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv

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

    # Importo las variables de entorno
    PREFIX = os.getenv("DISCORD_PREFIX")
    TOKEN = os.getenv("DISCORD_TOKEN")

    bot = commands.Bot(
        command_prefix=commands.when_mentioned_or(PREFIX),
        description='Relatively simple music bot example',
        help_command=None
    )

    # Lista de módulos activa
    bot.add_cog(modules.Help(bot))
    bot.add_cog(modules.General(bot))
    bot.add_cog(modules.Scheduler(bot))

    if TOKEN == None:
        log.info('Token not found ...')
        sys.exit(0)
    log.info('Bot started ...')
    bot.run(TOKEN)
