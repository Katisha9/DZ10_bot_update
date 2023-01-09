from bot_config import dp, bot
from aiogram import types
from random import randint
from pytube import YouTube
from aiogram.types import ReplyKeyboardRemove, \
        ReplyKeyboardMarkup, KeyboardButton, \
        InlineKeyboardMarkup, InlineKeyboardButton
total = 150
turn = 1
text = ''
@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    await bot.send_message(message.from_user.id, text=f'{message.from_user.first_name}, '
                                                      f'начинаем игру "Отними у младенца леденцы🍭🍭🍭". '
                                                      f'Всего у малыша Lollipops_eater_bot 150 леденцов. '
                                                      f'Можно брать не больше 28 штук. '
                                                      f'Выиграет тот, кто заберет последние сладости')
    button_yes = KeyboardButton('Да 👍🏻')
    button_no = KeyboardButton('Нет 👎🏻')
    greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(button_yes, button_no)

    await message.reply('Ты любишь сладкое?', reply_markup=greet_kb)

@dp.message_handler(text=['Получить'])
async def yt_downloader(message: types.Message):
    await bot.send_message(message.from_user.id, text=f'Хорошо! {message.from_user.first_name}, '
                                                      f'Видео-ролик для победителя будет загружен на твой компьютер!')
    file_name = 'https://www.youtube.com/watch?v=0P9odR9_FQ4'
    yt_video = YouTube(file_name)
    yt_video.streams.filter(resolution='360p', file_extension='mp4').first().download()

@dp.message_handler(text=['Да 👍🏻', 'Нет 👎🏻'])
async def start_play(message: types.Message):
    global total
    global turn
    total = 150
    if message.text:
        await bot.send_message(message.from_user.id, text=f'Хорошо! {message.from_user.first_name}, '
                                                          f'определим, кто ходит первым 🎲🎲')
        turn = randint(0, 1)  # жеребьевка очередности
        if turn == 1:
            await bot.send_message(message.from_user.id, text=f'{message.from_user.first_name}, первый ход у тебя')
            await bot.send_message(message.from_user.id,
                                   text=f'{message.from_user.first_name}, сколько хочешь леденцов?')
        else:
            await bot.send_message(message.from_user.id, text=f'{message.from_user.first_name},'
                                                              f' первый ход у Lollipops_eater_bot')
            loll = randint(1, 28)
            total -= int(loll)
            await bot.send_message(message.from_user.id, f'Младенец съел {loll}  🍭 и теперь у него осталось: {total}')
            await bot.send_message(message.from_user.id,
                                   text=f'{message.from_user.first_name}. Сколько ты хочешь взять?')
            turn = 1

@dp.message_handler()
async def anything(message: types.Message):
    global total
    global turn
    if turn == 1 and total > 28:
        if message.text.isdigit() and 0 < int(message.text) < 29:
            total -= int(message.text)
            await bot.send_message(message.from_user.id, f'{message.from_user.first_name}, отнять у младенца {message.text}🍭 - это как? '
                                                         f'У него осталось: {total}')
            turn = 0
        if message.text.isdigit() and int(message.text) >= 29:
            await message.reply(f'{message.from_user.first_name} да ты жадина! Можно взять от 1 до 28 штук')
            await bot.send_message(message.from_user.id, text=f'{message.from_user.first_name}. '
                                                              f'Сколько ты хочешь опять взять?')
    if turn == 0 and total > 28:
        await bot.send_message(message.from_user.id, f'Детеныш рыдает 😭😭😭')
        loll = randint(1, 28)
        total -= int(loll)
        await bot.send_message(message.from_user.id, f'Младенец съел {loll} 🍭 и теперь у него осталось: {total}')
        if total > 28:
            await bot.send_message(message.from_user.id, text=f'{message.from_user.first_name}. '
                                                              f'Сколько ты хочешь опять взять?')
        turn = 1
    if message.text.isdigit() and turn == 1 and total <= 28:
        await bot.send_message(message.from_user.id,
                               f'{message.from_user.first_name}, приятно отнимать у младенца последние {total} 🍭?')
        button_want = KeyboardButton('Получить')
        greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_want)
        await message.reply('Ты победил! Нажми, "Получить" свой видео-приз', reply_markup=greet_kb)

    if turn == 0 and total <= 28:
        await bot.send_message(message.from_user.id, f'{message.from_user.first_name}, младенец доел последние {total}'
                                                     f' 🍭 и победил!')


