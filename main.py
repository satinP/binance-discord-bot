import os
import discord

from discord.ext import tasks
from dotenv import load_dotenv
from binance.client import Client

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
API_KEY = os.environ.get("API_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")

binance_client = Client(API_KEY, SECRET_KEY)

discord_client = discord.Client()

@tasks.loop(minutes=1)
async def send_avg_price_message():

    ''' The channel id to receive bot messages: 
        Right click discord channel and select "Copy ID" 
    '''
    channel = discord_client.get_channel(id=834450097404117072) 

    crypto = "DOGE"
    coin = "BRL"
    symbol = crypto + coin

    try:
        response = binance_client.get_avg_price(symbol=symbol)
    except:
        await channel.send('Não foi possível acessar o binance_client')

    mins = response['mins']
    price = response['price']

    await channel.send(f'O preço médio da crypto **{crypto}** é de **{price} *{coin}* **.')

@discord_client.event
async def on_ready():
    send_avg_price_message.start()

discord_client.run(TOKEN)