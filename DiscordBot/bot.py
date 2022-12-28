import lightbulb

bot = lightbulb.BotApp(token = open('./tokens/tokens.txt','r').read(),
                       default_enabled_guilds=(int(open('./tokens/ds_channel_id.txt','r').read())))

@bot.command
@lightbulb.command('msg_intro','Saudação do bot')
@lightbulb.implements(lightbulb.SlashCommand)
async def hello(ctx):
    await ctx.respond('*Hey, eu sou o bot do Chico!*')

#Temperatura
import requests
import string

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = open('./tokens/api_weather_key.txt', 'r').read()

def kelvin_to_celsius(kelvin):
    celsius = kelvin - 273.15
    return celsius

@bot.command
@lightbulb.option('pais', 'País', type=str)
@lightbulb.option('cidade', 'Cidade', type=str)
@lightbulb.command('temperatura', 'Informe uma cidade seu país para saber a temperatura atual')
@lightbulb.implements(lightbulb.SlashCommand)
async def temperatura(ctx):
    country = ctx.options.pais
    CITY = string.capwords(ctx.options.cidade) + "," + country[0:2].lower()

    url = BASE_URL + "q=" + CITY + "&APPID=" + API_KEY 
    response = requests.get(url).json()

    temp_kelvin = response['main']['temp']
    umidade = response['main']['humidity']
    vento = response['wind']['speed']

    temp_celsius = str(round(kelvin_to_celsius(temp_kelvin)))

    await ctx.respond(f"```A temperatura atual em {string.capwords(ctx.options.cidade)} é de {temp_celsius} ºC \numidade do ar: {umidade}% \nvento: {vento} m/s```")

## Imports
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import lxml
import pandas
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, date
import pytz 
import sched
import schedule
import time
import smtplib

## Função para buscar cotações
def getCotacao(tickers):
  tickers = tickers.split(" ")  
  session = HTMLSession()
  mensagem_cotacoes = ""
  for ticker in tickers:    
    link = session.get('https://www.google.com/search?q='+ticker)
    html = BeautifulSoup(link.text, 'lxml')
    valor = html.find('span', class_='IsqQVc')
    cotacao = f"A cotação mais recente do ativo {ticker} é R${valor.text}\n"
    mensagem_cotacoes += cotacao
  return mensagem_cotacoes

#tickers = getTickers()
def func(tickers):
    cotacoes = getCotacao(tickers)
    return cotacoes

def acoesBot():
    schedule.every(1).minute.do(func)
    while True:
        schedule.run_pending()

@bot.command
@lightbulb.option('ativos', 'Ativos', type=str)
@lightbulb.command('cotação','Informe a lista de ativos separados por espaço. Exemplo:\nHGLG11 ENBR3')
@lightbulb.implements(lightbulb.SlashCommand)
async def hello(ctx):
    ativos = ctx.options.ativos
    cotacoes = func(ativos)
    await ctx.respond(cotacoes)


    
bot.run()