import os
import telebot
import threading
import yfinance as yf
from time import sleep

BOT_TOKEN = ""
BOT_INTERVAL = 3
BOT_TIMEOUT = 30

bot = telebot.TeleBot(BOT_TOKEN) #Generate new bot instance

def bot_polling():
    #global bot #Keep the bot object as global variable if needed
    print("Starting bot polling now")
    while True:
        try:
            print("New bot instance started")
            # botactions(bot) #If bot is used as a global variable, remove bot as an input param
            bot.polling(none_stop=True, interval=BOT_INTERVAL, timeout=BOT_TIMEOUT)
        except Exception as ex: #Error in polling
            print("Bot polling failed, restarting in {}sec. Error:\n{}".format(BOT_TIMEOUT, ex))
            bot.stop_polling()
            sleep(BOT_TIMEOUT)
        else: #Clean exit
            bot.stop_polling()
            print("Bot polling loop finished")
            break #End loop

@bot.message_handler(commands=['unnati'])
def unnati(message):
    bot.send_message(message.chat.id, "Hi,Unnati Thank you for being my creators partner hope you two will be spectacular partners\n\nGood Luck")

@bot.message_handler(commands=['snehal'])
def snehal(message):
    bot.send_message(message.chat.id, "I am a Computer Science geek who loves to explore and create new stuffs\n\n\n\nLinkedIn:https://www.linkedin.com/in/snehal-s-aa275818b/\nGithub:https://github.com/SNEHAL311998")\

@bot.message_handler(commands=['courses'])
def courses(message):
    bot.send_message(message.chat.id, "Top 5 websites to learn a new skill\n\nCodeacademy:https://www.codecademy.com/\nCoursera:https://www.coursera.org/\nUdemy:https://www.udemy.com/\nUdacit:https://www.udacity.com/\nEdx:https://www.edx.org/")

@bot.message_handler(commands=['👍'])
def like(message):
    bot.send_message(message.chat.id, "I hope you like this bot that I've made.Thank you for using it.")

@bot.message_handler(commands=['greet'])
def greet(message):
    bot.send_message(message.chat.id, "Hi, how is it going?.I am Lallu the Trade Bot.\n\nI give you all the information about current stock prices of various companies\n\nNo idea what to search\n\nHere are some suggestions from myside which I could help you with\n\n Try searching for:\n\n1.TESLA:price tsla\n2.BTC_USD:price btc-usd\n3.DODGE_COIN:price doge-usd\n4.ETHERIUM:price eth-usd\n\nStill dont have idea what to find:try -https://finance.yahoo.com/cryptocurrencies and search for their respective keywords\n\nTrending-tickers:https://finance.yahoo.com/trending-tickers\n\nMost active stocks:https://finance.yahoo.com/most-active\n\n\ncreator:SNEHAL\nFollow:@Lemon_Juice31\n\nDifferent commands available:\n/snehal\n/courses")

@bot.message_handler(commands=['wsb'])
def get_stocks(message):
  response = ""
  stocks = ['gme', 'amc', 'nok']
  stock_data = []
  for stock in stocks:
    data = yf.download(tickers=stock, period='2d', interval='1d')
    data = data.reset_index()
    response += f"-----{stock}-----\n"
    stock_data.append([stock])
    columns = ['stock']
    for index, row in data.iterrows():
      stock_position = len(stock_data) - 1
      price = round(row['Close'], 2)
      format_date = row['Date'].strftime('%m/%d')
      response += f"{format_date}: {price}\n"
      stock_data[stock_position].append(price)
      columns.append(format_date)
    print()

  response = f"{columns[0] : <10}{columns[1] : ^10}{columns[2] : >10}\n"
  for row in stock_data:
    response += f"{row[0] : <10}{row[1] : ^10}{row[2] : >10}\n"
  response += "\nStock Data"
  print(response)
  bot.send_message(message.chat.id, response)

def stock_request(message):
  request = message.text.split()
  if len(request) < 2 or request[0].lower() not in "price":
    return False
  else:
    return True

@bot.message_handler(func=stock_request)
def send_price(message):
  request = message.text.split()[1]
  data = yf.download(tickers=request, period='5m', interval='1m')
  if data.size > 0:
    data = data.reset_index()
    data["format_date"] = data['Datetime'].dt.strftime('%m/%d %I:%M %p')
    data.set_index('format_date', inplace=True)
    print(data.to_string())
    bot.send_message(message.chat.id, data['Close'].to_string(header=False))
  else:
    bot.send_message(message.chat.id, "No data!?")


bot_polling()
