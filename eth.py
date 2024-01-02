import telebot
import requests

TOKEN = "" #telegram bot token
ETHERSCAN_API_KEY = "" #sign up to etherscan.io and get api key
WALLET_ADDRESS = "" #eth adress

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "working")

@bot.message_handler(commands=['price'])
def get_eth_price(message):
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    response = requests.get(url).json()
    price = response["ethereum"]["usd"]
    bot.reply_to(message, f"{price} USD")

@bot.message_handler(commands=['bal'])
def get_eth_balance(message):
    url_price = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    response_price = requests.get(url_price).json()
    eth_price = response_price["ethereum"]["usd"]

    url_balance = "https://api.etherscan.io/api"
    params = {
        "module": "account",
        "action": "balance",
        "address": WALLET_ADDRESS,
        "tag": "latest",
        "apikey": ETHERSCAN_API_KEY
    }

    try:
        response_balance = requests.get(url_balance, params=params).json()
        balance_wei = int(response_balance["result"])
        balance_eth = balance_wei / 1e18
        balance_usd = balance_eth * eth_price
        bot.reply_to(message, f"{balance_eth} ETH, {balance_usd} USD")
    except Exception as e:
        bot.reply_to(e)

bot.polling()
