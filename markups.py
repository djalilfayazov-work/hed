from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup,  KeyboardButton


class Keyboard:
    class Main:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)

        hed    = KeyboardButton('🦔 Мой ёж')
        go     = KeyboardButton('👣 Перемещение')

        markup.add(hed, go)

    class Move:
        markup  = ReplyKeyboardMarkup(resize_keyboard=True)

        forest  = KeyboardButton('🌲 В лес')
        monster = KeyboardButton('👻 На охоту')
        tent    = KeyboardButton('⛺️ Лагерь')
        # lake    = KeyboardButton('🎣 На рыбалку')
        mine    = KeyboardButton('⛏ В шахту')

        back    = KeyboardButton('🔙 Главная')

        markup.add(forest, monster)
        markup.add(tent)
        markup.add(mine)
        markup.add(back)

    class Profile:
        markup    = ReplyKeyboardMarkup(resize_keyboard=True)

        inventory = KeyboardButton('📦 Склад')
        auc       = KeyboardButton('🛒 Аукцион')

        craft     = KeyboardButton('🛠 Верстак')
        potion    = KeyboardButton('🧪 Варить зелья')

        games     = KeyboardButton('♦️ Азартные игры')

        back      = KeyboardButton('🔙 Главная')
        go        = KeyboardButton('👣 Перемещение')

        markup.add(inventory, auc)
        markup.add(craft, potion)
        markup.add(games)
        markup.add(back, go)

    class Potion:
        markup     = ReplyKeyboardMarkup(resize_keyboard=True)

        health     = KeyboardButton('❤️ Асцидиева живучесть')
        energy     = KeyboardButton('⚡️ Энергетик')
        power      = KeyboardButton('💪 Слоновья ярость')
        protection = KeyboardButton('🛡 Черепашья мощь')
        # luck       = KeyboardButton('🍀 Удача Ямагучи')

        go         = KeyboardButton('👣 Перемещение')
        back       = KeyboardButton('🔙 Главная')

        markup.add(health)
        markup.add(energy)
        markup.add(power)
        markup.add(protection)
        markup.add(go, back)
    
    class PotionDone:
        health     = InlineKeyboardMarkup().add(
            InlineKeyboardButton('💊 Сварить', callback_data='health')
        )
        power      = InlineKeyboardMarkup().add(
            InlineKeyboardButton('💊 Сварить', callback_data='power')
        )
        protection = InlineKeyboardMarkup().add(
            InlineKeyboardButton('💊 Сварить', callback_data='protection')
        )
        # luck       = InlineKeyboardMarkup().add(
        #     InlineKeyboardButton('💊 Сварить', callback_data='luck')
        # )
        energy     = InlineKeyboardMarkup().add(
            InlineKeyboardButton('💊 Сварить', callback_data='energy')
        )