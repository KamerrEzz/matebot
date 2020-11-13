# -*- coding: utf-8 -*-

import os
import logging
import asyncio
import discord
from discord.ext import commands
import tweepy

log = logging.getLogger(__name__)

class Events(commands.Cog):
    """
    Módulo Events

    Se encarga de emitir en un canal específico de discord los tweets
    publicados de forma automática en real time
    """
    def __init__(self, bot):
        self.bot = bot

        # Defino un canal especifico para publicar los avisos
        self.events_channel_id = int(os.getenv("EVENTS_CHANNEL_ID"))

        # Se obtienen los valores correspondientes para la autenticación
        consumer_key        = os.getenv("TWITTER_API_KEY")
        consumer_secret     = os.getenv("TWITTER_API_SECRET_KEY")
        access_token        = os.getenv("TWITTER_ACCESS_TOKEN")
        access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

        # Proceso de autenticación de la cuenta de twitter developer necesaria para utilizar la API
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        # Llamado a la API con el argumento auth que es la autorización, y espera alcanzar el limite de velocidad.
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        # Creación de un objeto de tipo TweetsListener
        stream = TweetsListener(
            discord_post=self.discord_post,
            loop=asyncio.get_event_loop()
        )

        # Escucha la cuenta de twitter en búsqueda de nuevos twitts
        self.streamingApi = tweepy.Stream(auth=api.auth, listener=stream)

        # Busca en la cuenta especificada los tweets con el hashtag definido
        hashtag = os.getenv("TWITTER_HASHTAG")
        self.streamingApi.filter(
            track=[hashtag],
            is_async=True
        )

    async def discord_post(self, url):
        # Publica el tweet con un mesanje @everyone
        log.info("Twitter post")
        msg = "@everyone"
        channel = self.bot.get_channel(self.events_channel_id)
        await channel.send(f"{msg} {url}")

class TweetsListener(tweepy.StreamListener):
    def __init__(self, discord_post, loop, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Funcion definida en la clase News
        self.discord_post = discord_post
        self.loop = loop

    def on_connect(self):
        # Me avisa que se conectó y todo esta OK
        log.info("Connected to Twitter!")

    def on_status(self, status):
        # Si se quiere guardar el tweet en una BD para procesamiento se debe hacer en esta función
        # Ésta función procesa los tweets en tiempo real

        # Obtengo el id del tweet
        id_tweet = status.id
        # Creo el link al tweet con una cuenta determinada
        url_tweet = f"https://twitter.com/ljgago/status/{id_tweet}"

        # Envío el mensaje
        self.send_message(url_tweet)

    def send_message(self, msg):
        asyncio.run_coroutine_threadsafe(
            self.discord_post(msg),
            self.loop
        )

    def on_error(self, status_code):
        # Función que actúa frente a errores de conexión
        log.info("Error: %s", status_code)
