import telebot
import parseWB
import parseItemWb
import pandas as pd
from telebot import types

token='6778430105:AAEZ9xScoe5iXCP0juDCTKDF2CzwAaToP6I'
bot=telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'help','помощь','начать','about'])
def send_welcome(message):

	bot.send_message(message.chat.id, "Привет👋. Я бот для парсинга маркетплейса Wildberries🍒\n"
									  "Вот мои функции⬇️:\n"
									  "Информация о товаре (по ссылке)\n"
									  "Таблица с товарами бренда (по ссылке)\n"
									  "Таблица с товарами продавца (по ссылке)\n"
									  "Таблица с товарами поискового запроса (запрос)\n"
									  "Для работы бота отправьте ссылку, а затем выберите действие🤖.")

@bot.message_handler()
def info(message):
	markup = types.InlineKeyboardMarkup()
	btn1 = types.InlineKeyboardButton('Информация о товаре (ссылка)', callback_data='ParseItemWb')
	btn2 = types.InlineKeyboardButton('Список товаров поискового запроса (запрос)', callback_data='ParseSearchWb')
	btn3 = types.InlineKeyboardButton('Список товаров бренда (ссылка)', callback_data='ParseBrandWb')
	btn4 = types.InlineKeyboardButton('Список товаров продавца (ссылка)', callback_data='ParseSellerWb')
	markup.row(btn1)
	markup.row(btn2)
	markup.row(btn3)
	markup.row(btn4)
	bot.send_message(message.chat.id, 'Выберите действие🧐', reply_markup=markup)
	global text_zaprosa
	text_zaprosa = (message.text)
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
	if callback.data == 'ParseItemWb':
		print(text_zaprosa)
		try:
			bot.send_message(callback.message.chat.id, text='Выполняю...🤯')
			parseItemWb.Parser(text_zaprosa).parse()
			parseItemWb.Parser(text_zaprosa).parse_price()
			c = open('data.csv', 'rb')
			bot.send_document(callback.message.chat.id, c)
			read_file = pd.read_csv('data.csv')
			read_file.to_excel('data.xlsx', index=None, header=True)
			a = open('data.xlsx', 'rb')
			b = open('dataPrice.csv', 'rb')
			bot.send_document(callback.message.chat.id, a)
			bot.send_document(callback.message.chat.id, b)
			read_file = pd.read_csv('dataPrice.csv')
			read_file.to_excel('dataPrice.xlsx', index=None, header=True)
			d = open('dataPrice.xlsx', 'rb')
			bot.send_document(callback.message.chat.id, d)
		except Exception:
			bot.send_message(callback.message.chat.id, text='Произошла ошибка, попробуйте снова😢. Помощь /help')

	elif callback.data == 'ParseSearchWb':
		print(text_zaprosa)
		try:
			bot.send_message(callback.message.chat.id, text='Выполняю...🤯')
			parseWB.ParserSearch(text_zaprosa).parse()
			a = open('data.csv', 'rb')
			bot.send_document(callback.message.chat.id, a)
			read_file = pd.read_csv('data.csv')
			read_file.to_excel('data.xlsx', index=None, header=True)
			b = open('data.xlsx', 'rb')
			bot.send_document(callback.message.chat.id, b)
			c = open('statistics.csv', 'rb')
			bot.send_document(callback.message.chat.id, c)
			read_file = pd.read_csv('statistics.csv')
			read_file.to_excel('statistics.xlsx', index=None, header=True)
			d = open('statistics.xlsx', 'rb')
			bot.send_document(callback.message.chat.id, d)
		except Exception:
			bot.send_message(callback.message.chat.id, text='Произошла ошибка, попробуйте снова😢. Помощь /help')

	elif callback.data == 'ParseBrandWb':
		print(text_zaprosa)
		try:
			bot.send_message(callback.message.chat.id, text='Выполняю...🤯')
			parseWB.ParserBrand(text_zaprosa).parse()
			a = open('data.csv', 'rb')
			bot.send_document(callback.message.chat.id, a)
			read_file = pd.read_csv('data.csv')
			read_file.to_excel('data.xlsx', index=None, header=True)
			b = open('data.xlsx', 'rb')
			bot.send_document(callback.message.chat.id, b)
			c = open('statistics.csv', 'rb')
			bot.send_document(callback.message.chat.id, c)
			read_file = pd.read_csv('statistics.csv')
			read_file.to_excel('statistics.xlsx', index=None, header=True)
			d = open('statistics.xlsx', 'rb')
			bot.send_document(callback.message.chat.id, d)
		except Exception:
			bot.send_message(callback.message.chat.id, text='Произошла ошибка, попробуйте снова😢. Помощь /help')

	elif callback.data == 'ParseSellerWb':
		print(text_zaprosa)
		try:
			bot.send_message(callback.message.chat.id, text='Выполняю...🤯')
			parseWB.ParserSeller(text_zaprosa).parse()
			a = open('data.csv', 'rb')
			bot.send_document(callback.message.chat.id, a)
			read_file = pd.read_csv('data.csv')
			read_file.to_excel('data.xlsx', index=None, header=True)
			b = open('data.xlsx', 'rb')
			bot.send_document(callback.message.chat.id, b)
			c = open('statistics.csv', 'rb')
			bot.send_document(callback.message.chat.id, c)
			read_file = pd.read_csv('statistics.csv')
			read_file.to_excel('statistics.xlsx', index=None, header=True)
			d = open('statistics.xlsx', 'rb')
			bot.send_document(callback.message.chat.id, d)
		except Exception:
			bot.send_message(callback.message.chat.id, text='Произошла ошибка, попробуйте снова😢. Помощь /help')


bot.infinity_polling()