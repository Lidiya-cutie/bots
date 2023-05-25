from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

b1 = KeyboardButton(text='Hard')
b2 = KeyboardButton(text='Medium')
b3 = KeyboardButton(text='Light')
b4 = KeyboardButton(text='Menu')

kb_client.add(b1).add(b2)
kb_client.add(b3).add(b4)

kb_play = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
buttons = ["Поиграем?", "Не до игр"]
kb_play.add(*buttons)

kb_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb1 = KeyboardButton(text='password')
kb2 = KeyboardButton(text='play')
kb3 = KeyboardButton(text='dice')
kb4 = KeyboardButton(text='text')

kb_menu.add(kb1).insert(kb2)
kb_menu.add(kb3).insert(kb4)

kb_return_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

b_return = KeyboardButton(text='Main menu')

kb_return_menu.add(b_return)