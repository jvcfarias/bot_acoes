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

#The mail addresses and password
sender_address = 'bot.de.acoes@gmail.com'
sender_pass = 'vyouyefvublcfjfr'
receiver_address = 'fcpbarross@gmail.com' #Só mudar aqui se quiser testar no seu


## Função para receber os tickers e organizar em uma lista
## Isso aqui está feito de forma simples mesmo. Para um momento futuro a gente
## pode adicionar checagem se o ticker existe e etc
def getTickers():
  flag = True
  tickers = []
  while(flag):
    ticker = input("Informe o código do ticker: ")
    ticker = ticker.upper()
    tickers.append(ticker)
    if len(tickers) > 1:
      flag = False
  print(tickers)
  return tickers

## Função para buscar cotações
def getCotacao(tickers):
  session = HTMLSession()
  mensagem_cotacoes = ""
  for ticker in tickers:    
    link = session.get('https://www.google.com/search?q='+ticker)
    html = BeautifulSoup(link.text, 'lxml')
    valor = html.find('span', class_='IsqQVc')
    cotacao = f"A cotação mais recente do ativo {ticker} é R${valor.text}\n"
    mensagem_cotacoes += cotacao
  print(mensagem_cotacoes)
  return mensagem_cotacoes
    
## Função para checar se é dia da semana
## Posteriormente pensar em possibilidade de excluir feriados baseado em algum 
## calendário disponível on-line
def businessDay():
  time_zone = pytz.timezone("Brazil/East")
  time_now = datetime.now(time_zone)
  current_date = time_now.date()
  week_day = current_date.weekday()
  if week_day >= 2 and week_day <= 5:
    week_day = True
  else:
    week_day = False

#tickers = getTickers()
def func():
    tickers = ["HGLG11","BCFF11"]
    email_msg = getCotacao(tickers)
    email = montar_email(email_msg)
    enviar_email(email)
    
## Função para montar o email
def montar_email(mensagem_cotacoes):
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Cotações Atualizadas'
    #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mensagem_cotacoes, 'plain'))
    return message

## Função para enviar o email
def enviar_email(message):
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()    

schedule.every(1).minute.do(func)

while True:
    schedule.run_pending()


