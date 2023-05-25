import config
import os
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.markdown import text
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import keyboard as kb
import numpy as np
from numpy import argmax
import random

from keyboards import kb_client, kb_menu, kb_play, kb_return_menu
import matplotlib.pyplot as plt
#%matplotlib inline
#import librosa
#import librosa.display
import IPython.display
from PIL import Image


HELP_COMMAND = '''
/help - 
/start
/test1
/test2
/test3
/dice - При вызове команды /dice бот отправит в тот же чат игральный кубик.
/password
'''
# Присваивание токена       
b = Bot(config.TOKEN)
dp = Dispatcher(b)
TOKEN = os.getenv(config.TOKEN)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await b.send_message(chat_id=message.from_user.id,
                                   text = 'Добро пожаловать!\nИспользуй /help, '
                                   'чтобы узнать список доступных команд!')
    await message.delete()

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(text=HELP_COMMAND)
    await message.delete()

@dp.message_handler(commands=['password'])
async def start_password_command(message: types.Message):
    await b.send_message(chat_id=message.from_user.id,
                         text='Привет, я генератор паролей. На выбор имеется 3 варианта генерации паролей: сложный, средний, легкий.',
                         reply_markup=kb_client)
    await message.delete()

@dp.message_handler(commands=['help'])
async def start(message: types.Message):
    await message.reply('all commands = /gen/help')

@dp.message_handler(commands=['dice'])
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲", reply_markup=kb_return_menu)
    await message.delete()

@dp.message_handler(commands=['menu'])
async def open_main_menu(message: types.Message):
    await message.answer(text='Добро пожаловать в главное меню!',
                         reply_markup=kb_menu)
    await message.delete()    

@dp.message_handler(Text(equals='Menu'))
async def open_kb(message: types.Message):
    await message.answer(text='Добро пожаловать в главное меню!',
                         reply_markup=kb_menu)
    await message.delete()

@dp.message_handler(Text(equals='Main menu'))
async def open_kb(message: types.Message):
    await message.answer(text='Добро пожаловать в главное меню!',
                         reply_markup=kb_menu)
    await message.delete()   

@dp.message_handler(Text(equals='password'))
async def start_password_command(message: types.Message):
    await b.send_message(chat_id=message.from_user.id,
                         text='Привет, я генератор паролей. На выбор имеется 3 варианта генерации паролей: сложный, средний, легкий.',
                         reply_markup=kb_client)
    await message.delete() 

@dp.message_handler(Text(equals='Hard'))
async def passgen_hard(message: types.Message):
    try:
        password = ''
        alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        digits = '1234567890'
        signs = '!@#$%&'
        sumlist = alphabet + digits + signs
        for i in range(1, 12):
            password += random.choice(sumlist)
        await message.reply('Ваш сложный пароль может быть таким\n ' 
                            + password 
                            + '\nРад быть полезен!', 
                            reply_markup=kb_return_menu)
        await message.delete()
    except:
        await message.reply('ERRORE')
        await message.delete()

@dp.message_handler(Text(equals='Medium'))
async def passgen_medium(message: types.Message):
    try:
        password = ''
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        digits = '1234567890'
        signs = '!@#$%&'
        sumlist = alphabet + digits + signs
        for i in range(1, 12):
            password += random.choice(sumlist)
        await message.reply('Ваш пароль средней сложности может быть таким\n ' 
                            + password 
                            + '\nРад быть полезен!',
                            reply_markup=kb_return_menu)
        await message.delete()
    except:
        await message.reply('ERRORE')
        await message.delete()

@dp.message_handler(Text(equals='Light'))
async def passgen_light(message: types.Message):
    try:
        password = ''
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        digits = '1234567890'
        sumlist = alphabet + digits
        for i in range(1, 8):
            password += random.choice(sumlist)
        await message.reply('Ваш простой пароль может быть таким\n ' 
                            + password 
                            + '\nРад быть полезен!',
                            reply_markup=kb_return_menu)
        await message.delete()
    except:
        await message.reply('ERRORE')
        await message.delete()

@dp.message_handler(commands=['test1'])
async def test_one_command(message: types.Message):
    await b.send_message(chat_id=message.from_user.id,
                         text="Привет! Я создан для конвертации голосового/аудио сообщения в текст и создания аудио из текста.", reply_markup=kb_play)

@dp.message_handler(Text(equals="Поиграем?"))
async def find_file_ids(message: types.Message):
    for file in os.listdir('music/'):
        if file.split('.')[-1] == 'ogg':
            f = open('music/' + file, 'rb')
            message = b.send_voice(message.chat.id, f, None)
            await b.send_message("Отлично!", message.chat.id, message.voice.file_id, reply_to_message_id=message.message_id, reply_markup=types.ReplyKeyboardRemove())
            await message.delete()

# Обработчик для документов и аудиофайлов
@dp.message_handler(content_types=['document', 'audio'])
def handle_document_audio(message):
    try:
        if message.content_type == 'document':  # wav
            print(message.document)

            file_info = b.get_file(message.document.file_id)
            downloaded_file = b.download_file(file_info.file_path)

            src = 'files/' + message.document.file_name
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)

            b.reply_to(message, "Пожалуй, я сохраню это")
        elif message.content_type == 'audio':  # mp3
            print(message.audio)

            file_info = b.get_file(message.audio.file_id)
            downloaded_file = b.download_file(file_info.file_path)

            # для Windows можно использовать пути вида files/ при условии, 
            # что каталог files находится рядом с файлом .py
            src = 'files/' + message.audio.file_name
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)

            b.reply_to(message, "Пожалуй, я сохраню это")
    except Exception as e:
        b.reply_to(message, str(e))

# ?
@dp.message_handler(Text(equals='dice'))
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲", reply_markup=kb_return_menu)
    await message.delete()

# моментально ответит пользователю той же гифкой, что была прислана:
@dp.message_handler(content_types=[types.ContentType.ANIMATION])
async def echo_document(message: types.Message):
    await b.message.reply_animation(message.animation.file_id)
    
# метод download() для загрузки небольших файлов на сервер, где запущен бот:
@dp.message_handler(content_types=[types.ContentType.DOCUMENT])
async def download_doc(message: types.Message):
    # Скачивание в каталог с ботом с созданием подкаталогов по типу файла
    await b.message.document.download()

# Типы содержимого тоже можно указывать по-разному.
@dp.message_handler(content_types=["photo"])
async def download_photo(message: types.Message):
    # Убедись, что каталог /tmp/somedir существует!
    await b.message.photo[-1].download(destination="/tmp/somedir/")
    pass

#
import aiogram.utils.markdown as fmt

@dp.message_handler(commands="test2")
async def with_hidden_link(message: types.Message):
    await b.message.answer(
        f"{fmt.hide_link('https://telegram.org/blog/video-calls/ru')}Кто бы мог подумать, что "
        f"в 2020 году в Telegram появятся видеозвонки!\n\nОбычные голосовые вызовы "
        f"возникли в Telegram лишь в 2017, заметно позже своих конкурентов. А спустя три года, "
        f"когда огромное количество людей на планете приучились работать из дома из-за эпидемии "
        f"коронавируса, команда Павла Дурова не растерялась и сделала качественные "
        f"видеозвонки на WebRTC!\n\nP.S. а ещё ходят слухи про демонстрацию своего экрана :)",
        parse_mode=types.ParseMode.HTML)

@dp.message_handler(content_types=["text"])
async def get_text_messages(message: types.Message): 
    if message.text.lower() == 'привет' or message.text.lower() == 'ru' or message.text.lower() == 'старт':
        await message.answer('Привет!')

    elif message.text.lower() == "hi" or message.text.lower() == 'eng':
        await message.answer('Hello! I am cutie_new_bot. How can i help you?')

    elif message.text.lower() == 'как дела?' or message.text.lower() == 'как твои дела?':
        await message.answer("У меня все отлично! А как твои дела?")
    
    elif message.text.lower() == 'how are you?' or message.text.lower() == 'how are u?':
        await message.answer("I'm fine, thanks. And you?")
    
    else:
        await message.answer('Sorry, i dont understand you.')


# 
if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True)
    except (KeyboardInterrupt, SystemExit):
        pass
    b.polling(none_stop=True, interval=0.5)
