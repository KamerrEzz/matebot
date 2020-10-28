import discord
from discord.ext import commands


class FAQ(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def invitacion(self, ctx):
        await ctx.send("Link de invitacion: discord.gg")

    @commands.command()
    async def invitacion(self, ctx):
        await ctx.send("Link de invitacion: discord.gg")


def setup(client):
    client.add_cog(FAQ(client))