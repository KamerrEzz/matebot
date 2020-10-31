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
    
    bot = commands.Bot(
        command_prefix=commands.when_mentioned_or("!"),
        description='Ayudaaa',
        help_command=None
    )

    # Lista de módulos activa
    bot.add_cog(modules.FAQ(bot))

    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")

    if TOKEN == None:
        log.info('Token not found ...')
        sys.exit(0)

    log.info('Bot started ...')
    bot.run(TOKEN)