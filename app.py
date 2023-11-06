from aiogram       import Bot, Dispatcher, executor
from aiogram.types import Message, CallbackQuery
from random        import randint, choice
from time          import sleep

from config        import Settings
from database      import DataBase
from markups       import Keyboard

from aiogram.types import ReplyKeyboardMarkup as km, KeyboardButton as kb
from aiogram.types import InlineKeyboardMarkup as im, InlineKeyboardButton as ib

""" --------------------------------------------------- """

conf = Settings()
db   = DataBase()
menu = Keyboard()

bot  = Bot(conf.token, parse_mode='html')
dp   = Dispatcher(bot)

""" --------------------------------------------------- """


@dp.message_handler(commands=['start'])
async def start(msg: Message):
    chat = msg.chat

    if chat.id > 0:
        if not db.check(chat.id):
            await msg.answer(
                conf.read('non').format(
                    chat.id, chat.first_name
                ),
                reply_markup=menu.Main.markup
            )

            db.add_user(chat.id)
        else:
            await msg.answer(
                conf.read('hello').format(
                    chat.id, chat.first_name
                ),
                reply_markup=menu.Main.markup
            )


@dp.message_handler(commands=['potions'])
async def potions(msg: Message):
    chat = msg.chat

    if chat.id > 0:
        if not db.check(chat.id):
            await msg.answer(
                conf.read('non').format(
                    chat.id, chat.first_name
                ),
                reply_markup=menu.Main.markup
            )

            db.add_user(chat.id)
        else:
            pass


@dp.message_handler(content_types=['text'])
async def get_text(msg: Message):
    chat = msg.chat

    if chat.id > 0:
        if not db.check(chat.id):
            await msg.answer(
                conf.read('non').format(
                    chat.id, chat.first_name
                ),
                reply_markup=menu.Main.markup
            )

            db.add_user(chat.id)
        else:

            match msg.text:
                case '🦔 Мой ёж':
                    hed_values = db.get(chat.id, 'users', '*')[1::]

                    hed_values.append(conf.weapon.get(db.get(chat.id, 'users', 'weapon')[0]))
                    hed_values.append(conf.armor.get(db.get(chat.id, 'users', 'armor')[0]))
                    hed_values.append(conf.pick.get(db.get(chat.id, 'users', 'pick')[0]))
                    hed_values.append(conf.row.get(db.get(chat.id, 'users', 'row')[0]))

                    await msg.answer(
                        conf.read('profile').format(
                            chat.id, chat.first_name,
                            *hed_values
                        )
                    )

                case '👣 Перемещение':
                    await msg.answer(
                        'Выберите место',
                        reply_markup=menu.Move.markup
                    )

                case '🔙 Главная':
                    await msg.answer(
                        'Главное меню',
                        reply_markup=menu.Main.markup
                    )


                case '⛺️ Лагерь':
                    db.set(chat.id, 'users', 'lock', 'Лагерь')
                    await msg.answer(
                        'Вы переместились в лагерь',
                        reply_markup=menu.Profile.markup
                    )

                case '📦 Склад':
                    if db.get(chat.id, 'users', 'lock')[0] == 'Лагерь':
                        inventory = [i for i in db.get(chat.id, 'items', '*')][1::]
                        inventory += [i for i in db.get(chat.id, 'potions', '*')][1::]
                        inventory += [i for i in db.get(chat.id, 'hunter', '*')][1::]
                        inventory += [i for i in db.get(chat.id, 'mine', '*')][1::]

                        await bot.send_message(
                            chat.id,
                            conf.read('inventory').format(
                                *inventory
                            )
                        )


                case '🌲 В лес':
                    db.set(chat.id, 'users', 'lock', 'Лес')
                    await msg.answer(
                        'Вы переместились в лес',
                        reply_markup=km(resize_keyboard=True, keyboard=[
                            [kb('Добыть ресурсы')],
                            [kb('👣 Перемещение'), kb('🔙 Главная')]
                        ])
                    )

                case 'Добыть ресурсы':
                    if db.get(chat.id, 'users', 'lock')[0] == 'Лес':
                        get_hp = db.get(chat.id, 'users', 'hp')[0]
                        if get_hp > 25:
                            items = [
                                [
                                    choice(conf.items.get('usual')), randint(1, 6)
                                ],
                                [
                                    choice(conf.items.get('usual')), randint(1, 5)
                                ],
                                [
                                    choice(conf.items.get('rare')), randint(1, 4)
                                ],
                                [
                                    choice(conf.items.get('uprare')), randint(1, 3)
                                ]
                            ]

                            text = conf.read('hed').format(
                                chat.first_name,

                                items[0][0], items[0][1],
                                items[1][0], items[1][1],
                                items[2][0], items[2][1],

                                conf.emoji.get(items[0][0]),
                                conf.emoji.get(items[1][0]),
                                conf.emoji.get(items[2][0])
                            )

                            db.add_item(chat.id, items[0][0], 'items', items[0][1])
                            db.add_item(chat.id, items[1][0], 'items', items[1][1])
                            db.add_item(chat.id, items[2][0], 'items', items[2][1])

                            if not choice([True, True, True, True, False]):
                                text += '\n{0}<b>{1}</b> — {2}'.format(
                                    conf.emoji.get(items[3][0]),
                                    items[3][0], items[3][1]
                                )
                                db.add_item(chat.id, items[3][0], 'items', items[3][1])

                            minch = randint(1, 4)

                            if minch == 4:
                                armor = conf.armor.get(db.get(chat.id, 'users', 'armor')[0])

                                if armor == 0:
                                    hp = randint(6, 7)
                                    text += f'\n\nВы потеряли очкои жизни : {hp}🖤'
                                    db.set_field(
                                        chat.id, 'hp', 'users',
                                        db.get(chat.id, 'users', 'hp')[0] - hp
                                    )

                                if armor == 50:
                                    hp = randint(5, 6)
                                    text += f'\n\nВы потеряли очкои жизни : {hp}🖤'
                                    db.set_field(
                                        chat.id, 'hp', 'users',
                                        db.get(chat.id, 'users', 'hp')[0] - hp
                                    )
                                if armor == 100:
                                    hp = randint(4, 5)
                                    text += f'\n\nВы потеряли очкои жизни : {hp}🖤'
                                    db.set_field(
                                        chat.id, 'hp', 'users',
                                        db.get(chat.id, 'users', 'hp')[0] - hp
                                    )
                                if armor == 250:
                                    hp = randint(3, 4)
                                    text += f'\n\nВы потеряли очкои жизни : {hp}🖤'
                                    db.set_field(
                                        chat.id, 'hp', 'users',
                                        db.get(chat.id, 'users', 'hp')[0] - hp
                                    )
                                if armor == 320:
                                    hp = randint(1, 3)
                                    text += f'\n\nВы потеряли очкои жизни : {hp}🖤'
                                    db.set_field(
                                        chat.id, 'hp', 'users',
                                        db.get(chat.id, 'users', 'hp')[0] - hp
                                    )

                            await bot.send_message(
                                chat.id,
                                text
                            )
                        else:
                            await bot.send_message(
                                chat.id,
                                f'Мало очков здоровья 🖤 [{get_hp}]\nСварите зелье асцидиевой жизни!'
                            )


                case '⛏ В шахту':
                    db.set(chat.id, 'users', 'lock', 'Шахта')
                    await msg.answer(
                        'Вы переместились в шахту',
                        reply_markup=km(resize_keyboard=True, keyboard=[
                            [kb('Добыть метал')],
                            [kb('👣 Перемещение'), kb('🔙 Главная')]
                        ])
                    )

                case 'Добыть метал':
                    if db.get(chat.id, 'users', 'lock')[0] == 'Шахта':
                        pick = conf.pick.get(db.get(chat.id, 'users', 'pick')[0])

                        sleep(pick)

                        items = [
                            [
                                choice(conf.mine.get('usual')), randint(300, 500)
                            ],
                            [
                                choice(conf.mine.get('usual')), randint(300, 500)
                            ],
                            [
                                choice(conf.mine.get('rare')), randint(100, 250)
                            ],
                            [
                                choice(conf.mine.get('uprare')), randint(10, 75)
                            ]
                        ]

                        text = conf.read('hed').format(
                            chat.first_name,

                            items[0][0], items[0][1],
                            items[1][0], items[1][1],
                            items[2][0], items[2][1],

                            conf.emoji.get(items[0][0]),
                            conf.emoji.get(items[1][0]),
                            conf.emoji.get(items[2][0])
                        )

                        db.add_item(chat.id, items[0][0], 'mine', items[0][1])
                        db.add_item(chat.id, items[1][0], 'mine', items[1][1])
                        db.add_item(chat.id, items[2][0], 'mine', items[2][1])

                        if not choice([True, True, True, True, False]):
                            text += '\n{0}<b>{1}</b> — {2}'.format(
                                conf.emoji.get(items[3][0]),
                                items[3][0], items[3][1]
                            )
                            db.add_item(chat.id, items[3][0], 'mine', items[3][1])

                        await bot.send_message(
                                chat.id,
                                text
                            )


                case '👻 На охоту':
                    db.set(chat.id, 'users', 'lock', 'Монстры')
                    await msg.answer(
                        'Вы переместились к монстрам',
                        reply_markup=km(resize_keyboard=True, keyboard=[
                            [kb('Охотиться')],
                            [kb('👣 Перемещение'), kb('🔙 Главная')]
                        ])
                    )

                case 'Охотиться':
                    if db.get(chat.id, 'users', 'lock')[0] == 'Монстры':
                        if randint(0, 1) == 1:  # 50/50 появление моба
                            # ниже шанс в 16.6% на выпадение эпического предмета
                            if not choice([True, True, True, True, True, False]):
                                item = choice(conf.mob_items.get('epic'))
                                await bot.send_message(
                                    chat.id,
                                    conf.read('mob').format(
                                        conf.mobs.get(item),
                                        item, 1, conf.emoji.get(item)
                                    )
                                )

                                db.add_item(chat.id, item, 'hunter', 1)
                            else:
                                shch = 1
                                await bot.send_message(
                                    chat.id,
                                    conf.read('mob').format(
                                        'Каньонный таракан 🐜',
                                        'Шестеренки', shch, '⚙️'
                                    )
                                )

                                db.add_item(chat.id, 'Шестеренки', 'items', shch)
                        else:
                            await bot.send_message(
                                chat.id, 'Вы не нашли мобов'
                            )


                case '♦️ Азартные игры':
                    if db.get(chat.id, 'users', 'lock')[0] == 'Лагерь':
                        await msg.answer(
                            'Посмотрим насколько ты крепок',
                            reply_markup=km(resize_keyboard=True, keyboard=[
                                [kb('Русская рулетка'), kb('Лотерейный билет')],
                                [kb('👣 Перемещение'), kb('🔙 Главная')]
                            ])
                        )

                case 'Русская рулетка':
                    if db.get(chat.id, 'users', 'lock')[0] == 'Лагерь':
                        await msg.answer(
                            'Выберите сумму для игры',
                            reply_markup=im(row_width=2, inline_keyboard=[
                                [ib('10$', callback_data='r10'),
                                 ib('100$', callback_data='r100')],
                                [ib('500$', callback_data='r500'),
                                 ib('1000$', callback_data='r1000')],
                            ])
                        )

                case 'Лотерейный билет':
                    if db.get(chat.id, 'users', 'lock')[0] == 'Лагерь':
                        await msg.answer(
                            'Хотите купить билет за $10 ??',
                            reply_markup=im(row_width=2, inline_keyboard=[
                                [ib('Купить', callback_data='l10')],
                            ])
                        )


                case '🛒 Аукцион':
                    if db.get(chat.id, 'users', 'lock')[0] == 'Лагерь':
                        auc = 'Все предметы на аукционе:\n\n'

                        for i in db.get_auc():
                            auc += conf.read('auc').format(
                                i[4], i[0], i[1], i[2], i[3], i[2] * i[3], conf.emoji.get(i[1])
                            )

                        await msg.answer(auc)

                case '/auc':
                    await msg.answer(
                        conf.read('aucc')
                    )


                case '🧪 Варить зелья':
                    if db.get(chat.id, 'users', 'lock')[0] == 'Лагерь':
                        await msg.answer(
                            'Выберите зелье ниже',
                            reply_markup=menu.Potion.markup
                        )

                case '💪 Слоновья ярость':
                    if db.get(chat.id, 'users', 'lock')[0] == 'Лагерь':
                        potion = 'Для варки зелья вам понадобиться:\n\n' \
                                 '🍓 <b>Малина</b> ~ 20 {0}\n' \
                                 '🍒 <b>Вишня</b> ~ 25 {1}\n' \
                                 '🫐 <b>Земляника</b> ~ 15 {2}\n' \
                                 '🦷 <b>Клык</b> ~ 3 {3}\n' \

                        isc = [
                            '✅' if db.get(chat.id, 'items', 'Малина')[0]    >= 20 else '❌', 
                            '✅' if db.get(chat.id, 'items', 'Вишня')[0]     >= 25 else '❌', 
                            '✅' if db.get(chat.id, 'items', 'Земляника')[0] >= 15 else '❌', 
                            '✅' if db.get(chat.id, 'hunter', 'Клык')[0]     >= 3  else '❌', 
                        ]

                        if isc != ['✅','✅','✅','✅']:
                            await msg.answer(
                                potion.format(*isc)
                            )
                        else:
                            await msg.answer(
                                potion.format(*isc),
                                reply_markup=menu.PotionDone.power
                            )

                case '🛡 Черепашья мощь':
                    if db.get(chat.id, 'users', 'lock')[0] == 'Лагерь':
                        potion = 'Для варки зелья вам понадобиться:\n\n' \
                                 '🍓 <b>Малина</b> ~ 15 {0}\n' \
                                 '🍒 <b>Вишня</b> ~ 20 {1}\n' \
                                 '🫐 <b>Земляника</b> ~ 30 {2}\n' \
                                 '🐢 <b>Панцирь</b> ~ 3 {3}\n' \

                        isc = [
                            '✅' if db.get(chat.id, 'items', 'Малина')[0]    >= 15 else '❌', 
                            '✅' if db.get(chat.id, 'items', 'Вишня')[0]     >= 20 else '❌', 
                            '✅' if db.get(chat.id, 'items', 'Земляника')[0] >= 30 else '❌', 
                            '✅' if db.get(chat.id, 'hunter', 'Панцирь')[0]  >= 3  else '❌', 
                        ]

                        if isc != ['✅','✅','✅','✅']:
                            await msg.answer(
                                potion.format(*isc)
                            )
                        else:
                            await msg.answer(
                                potion.format(*isc),
                                reply_markup=menu.PotionDone.protection
                            )

                case '🍀 Удача Ямагучи':
                    if db.get(chat.id, 'users', 'lock')[0] == 'Лагерь':
                        potion = 'Для варки зелья вам понадобиться:\n\n' \
                                 '🍓 <b>Малина</b> ~ 15 {0}\n' \
                                 '🍒 <b>Вишня</b> ~ 20 {1}\n' \
                                 '🫐 <b>Земляника</b> ~ 30 {2}\n' \
                                 '🧬 <b>Сгусток</b> ~ 3 {3}\n' \

                        isc = [
                            '✅' if db.get(chat.id, 'items', 'Малина')[0]    >= 15 else '❌', 
                            '✅' if db.get(chat.id, 'items', 'Вишня')[0]     >= 20 else '❌', 
                            '✅' if db.get(chat.id, 'items', 'Земляника')[0] >= 30 else '❌', 
                            '✅' if db.get(chat.id, 'hunter', 'Сгусток')[0]  >= 3  else '❌', 
                        ]

                        if isc != ['✅','✅','✅','✅']:
                            await msg.answer(
                                potion.format(*isc)
                            )
                        else:
                            await msg.answer(
                                potion.format(*isc),
                                reply_markup=menu.PotionDone.luck
                            )

                case '❤️ Асцидиева живучесть':
                    if db.get(chat.id, 'users', 'lock')[0] == 'Лагерь':
                        potion = 'Для варки зелья вам понадобиться:\n\n' \
                                 '🍓 <b>Малина</b> ~ 20 {0}\n' \
                                 '🍒 <b>Вишня</b> ~ 20 {1}\n' \
                                 '🫐 <b>Земляника</b> ~ 20 {2}\n' \
                                 '🌱 <b>Мох</b> ~ 3 {3}\n' \

                        isc = [
                            '✅' if db.get(chat.id, 'items', 'Малина')[0]    >= 20 else '❌', 
                            '✅' if db.get(chat.id, 'items', 'Вишня')[0]     >= 20 else '❌', 
                            '✅' if db.get(chat.id, 'items', 'Земляника')[0] >= 20 else '❌', 
                            '✅' if db.get(chat.id, 'hunter', 'Мох')[0]      >= 3  else '❌', 
                        ]

                        if isc != ['✅','✅','✅','✅']:
                            await msg.answer(
                                potion.format(*isc)
                            )
                        else:
                            await msg.answer(
                                potion.format(*isc),
                                reply_markup=menu.PotionDone.health
                            )

                case '⚡️ Энергетик':
                    if db.get(chat.id, 'users', 'lock')[0] == 'Лагерь':
                        potion = 'Для варки зелья вам понадобиться:\n\n' \
                                 '🍓 <b>Малина</b> ~ 20 {0}\n' \
                                 '🍒 <b>Вишня</b> ~ 20 {1}\n' \
                                 '🫐 <b>Земляника</b> ~ 20 {2}\n' \

                        isc = [
                            '✅' if db.get(chat.id, 'items', 'Малина')[0]    >= 20 else '❌', 
                            '✅' if db.get(chat.id, 'items', 'Вишня')[0]     >= 20 else '❌', 
                            '✅' if db.get(chat.id, 'items', 'Земляника')[0] >= 20 else '❌', 
                        ]

                        if isc != ['✅','✅','✅']:
                            await msg.answer(
                                potion.format(*isc)
                            )
                        else:
                            await msg.answer(
                                potion.format(*isc),
                                reply_markup=menu.PotionDone.energy
                            )


                case _:
                    response = msg.text.split(' ')
                    if len(response) == 4 and response[0].lower() == 'выставить':
                        try:
                            response[1] = response[1].capitalize()
                            response[2] = int(response[2])
                            response[3] = int(response[3])

                            
                            for k, v in conf.all_items.items():
                                if response[1] in v:
                                    if db.get(chat.id, k, response[1])[0] >= response[2]:
                                        db.bring(chat.id, response[1], k, response[2])
                                        db.set_auc(chat.id, response[1], response[2], response[3])
                                        await msg.answer(
                                            'Вы успешно выставили свой товар'
                                        )

                        except Exception as e:
                            print(e)

                    elif len(response) == 2 and response[0].lower() == 'купить':
                        try:
                            auc_item = db.item_auc(response[1])
                            if auc_item[0] != chat.id:
                                print(auc_item)
                                total_price = int(auc_item[2] * auc_item[3])
                                if db.get(chat.id, 'users', 'balance')[0] >= total_price:
                                    db.bring_auc(auc_item[4])

                                    for k, v in conf.all_items.items():
                                        if auc_item[1] in v:
                                            db.add_item(
                                                chat.id, auc_item[1],
                                                k, auc_item[2]
                                            )

                                    db.bring(
                                        id=chat.id,
                                        table='users',
                                        field='balance',
                                        amount=total_price
                                    )
                                    db.add_item(
                                        id=auc_item[0],
                                        table='users',
                                        field='balance',
                                        amount=total_price
                                    )

                                    await msg.answer(
                                        'Вы успешно приобрели предмет'
                                    )

                        except Exception as e:
                            print(e)

                    elif response[0] == '/text' and chat.id == 920747145:
                        response.remove('/text')

                        text = ' '.join(response)
                        text += f'\n\n<a href="tg://user?id={bot.id}"><b><u>[Сообщение через бота]</u></b></a>'

                        await msg.answer(
                            f'Отправка сообщения в канал:\n\n"{text}"',
                            reply_markup=im(row_width=2, inline_keyboard=[
                                [ib('Отправить', callback_data='isSend')],
                                [ib('Не отправлять', callback_data='notSend')]
                            ])
                        )
                        conf.isSend = text


@dp.callback_query_handler(text='r10')
async def get_text(call: CallbackQuery):
    chat = call.message.chat
    msg = call.message
    if chat.id > 0:
        if not db.check(chat.id):
            await msg.answer(
                conf.read('non').format(
                    chat.id, chat.first_name
                ),
                reply_markup=menu.Main.markup
            )

            db.add_user(chat.id)
        else:
            if db.get(chat.id, 'users', 'lock')[0] == 'Лагерь':
                if db.get(chat.id, 'users', 'balance')[0] >= 10:

                    try:
                        await msg.delete()
                    except Exception as e:
                        print(e)

                    if not choice([True, True, True, True, True, False]):
                        db.add_item(chat.id, 'balance', 'users', 10)

                        await msg.answer(
                            'Вы выиграли 10$'
                        )
                    else:
                        db.bring(id=chat.id, field='balance', table='users', amount=10)

                        await msg.answer(
                            'Вы проиграли 10$'
                        )

@dp.callback_query_handler(text='r100')
async def get_text(call: CallbackQuery):
    chat = call.message.chat
    msg = call.message
    if chat.id > 0:
        if not db.check(chat.id):
            await msg.answer(
                conf.read('non').format(
                    chat.id, chat.first_name
                ),
                reply_markup=menu.Main.markup
            )

            db.add_user(chat.id)
        else:
            if db.get(chat.id, 'users', 'lock')[0] == 'Лагерь':
                if db.get(chat.id, 'users', 'balance')[0] >= 100:

                    try:
                        await msg.delete()
                    except Exception as e:
                        print(e)

                    if not choice([True, True, True, True, True, False]):
                        db.add_item(chat.id, 'balance', 'users', 100)

                        await msg.answer(
                            'Вы выиграли 100$'
                        )
                    else:
                        db.bring(id=chat.id, field='balance', table='users', amount=100)

                        await msg.answer(
                            'Вы проиграли 100$'
                        )

@dp.callback_query_handler(text='r500')
async def get_text(call: CallbackQuery):
    chat = call.message.chat
    msg = call.message
    if chat.id > 0:
        if not db.check(chat.id):
            await msg.answer(
                conf.read('non').format(
                    chat.id, chat.first_name
                ),
                reply_markup=menu.Main.markup
            )

            db.add_user(chat.id)
        else:
            if db.get(chat.id, 'users', 'lock')[0] == 'Лагерь':
                if db.get(chat.id, 'users', 'balance')[0] >= 500:

                    try:
                        await msg.delete()
                    except Exception as e:
                        print(e)

                    if not choice([True, True, True, True, True, False]):
                        db.add_item(chat.id, 'balance', 'users', 500)

                        await msg.answer(
                            'Вы выиграли 500$'
                        )
                    else:
                        db.bring(id=chat.id, field='balance', table='users', amount=500)

                        await msg.answer(
                            'Вы проиграли 500$'
                        )

@dp.callback_query_handler(text='r1000')
async def get_text(call: CallbackQuery):
    chat = call.message.chat
    msg = call.message
    if chat.id > 0:
        if not db.check(chat.id):
            await msg.answer(
                conf.read('non').format(
                    chat.id, chat.first_name
                ),
                reply_markup=menu.Main.markup
            )

            db.add_user(chat.id)
        else:
            if db.get(chat.id, 'users', 'lock')[0] == 'Лагерь':
                if db.get(chat.id, 'users', 'balance')[0] >= 1000:

                    try:
                        await msg.delete()
                    except Exception as e:
                        print(e)

                    if not choice([True, True, True, True, True, False]):
                        db.add_item(chat.id, 'balance', 'users', 1000)

                        await msg.answer(
                            'Вы выиграли 1000$'
                        )
                    else:
                        db.bring(id=chat.id, field='balance', table='users', amount=1000)

                        await msg.answer(
                            'Вы проиграли 1000$'
                        )


@dp.callback_query_handler(text='l10')
async def get_text(call: CallbackQuery):
    chat = call.message.chat
    msg = call.message
    if chat.id > 0:
        if not db.check(chat.id):
            await msg.answer(
                conf.read('non').format(
                    chat.id, chat.first_name
                ),
                reply_markup=menu.Main.markup
            )

            db.add_user(chat.id)
        else:
            if db.get(chat.id, 'users', 'lock')[0] == 'Лагерь':
                if db.get(chat.id, 'users', 'balance')[0] >= 10:

                    db.bring(chat.id, 'balance', 'users', 10)

                    try:
                        await msg.delete()
                    except Exception as e:
                        print(e)

                    chs = []
                    for i in range(1, 101):
                        if i < 70: chs.append(2)
                        if i > 70 and i <= 87: chs.append(5)
                        if i > 87 and i <= 97: chs.append(10)
                        if i > 97: chs.append(1000)

                    prize = choice(chs)

                    await msg.answer(
                        f'Ваш приз {prize}$'
                    )

                    db.add_item(chat.id, 'balance', 'users', prize)

@dp.callback_query_handler(text='isSend')
async def send_channel(call: CallbackQuery):
    if call.message.chat.id == 920747145:
        await bot.send_message(
            conf.channel,
            conf.isSend
        )

        try:
            await call.message.delete()
        except Exception as e:
            print(e)

@dp.callback_query_handler(text='notSend')
async def send_channel(call: CallbackQuery):
    try:
        await call.message.delete()
    except Exception as e:
        print(e)


@dp.callback_query_handler(text='power')
async def potion(call : CallbackQuery):
    chat = call.message.chat
    msg = call.message
    if chat.id > 0:
        if not db.check(chat.id):
            await msg.answer(
                conf.read('non').format(
                    chat.id, chat.first_name
                ),
                reply_markup=menu.Main.markup
            )

            db.add_user(chat.id)
        else:
            if db.get(chat.id, 'users', 'lock')[0] == 'Лагерь':
                isc = [
                    '✅' if db.get(chat.id, 'items', 'Малина')[0]    >= 20 else '❌', 
                    '✅' if db.get(chat.id, 'items', 'Вишня')[0]     >= 25 else '❌', 
                    '✅' if db.get(chat.id, 'items', 'Земляника')[0] >= 15 else '❌', 
                    '✅' if db.get(chat.id, 'hunter', 'Клык')[0]     >= 3  else '❌', 
                ]

                if isc == ['✅','✅','✅','✅']:
                    try:
                        await msg.delete()
                    except Exception as e:
                        print(e)

                    await msg.answer(
                        'Вы успешно сварили зелье'
                    )

                    db.bring(chat.id, 'Малина', 'items', 20)
                    db.bring(chat.id, 'Вишня', 'items', 25)
                    db.bring(chat.id, 'Земляника', 'items', 15)
                    db.bring(chat.id, 'Клык', 'hunter', 3)

                    db.add_item(chat.id, 'power', 'potions', 1)

@dp.callback_query_handler(text='protection')
async def potion(call : CallbackQuery):
    chat = call.message.chat
    msg = call.message
    if chat.id > 0:
        if not db.check(chat.id):
            await msg.answer(
                conf.read('non').format(
                    chat.id, chat.first_name
                ),
                reply_markup=menu.Main.markup
            )

            db.add_user(chat.id)
        else:
            if db.get(chat.id, 'users', 'lock')[0] == 'Лагерь':
                isc = [
                    '✅' if db.get(chat.id, 'items', 'Малина')[0]    >= 15 else '❌', 
                    '✅' if db.get(chat.id, 'items', 'Вишня')[0]     >= 20 else '❌', 
                    '✅' if db.get(chat.id, 'items', 'Земляника')[0] >= 30 else '❌', 
                    '✅' if db.get(chat.id, 'hunter', 'Панцирь')[0]  >= 3  else '❌', 
                ]

                if isc == ['✅','✅','✅','✅']:
                    try:
                        await msg.delete()
                    except Exception as e:
                        print(e)

                    await msg.answer(
                        'Вы успешно сварили зелье'
                    )

                    db.bring(chat.id, 'Малина', 'items', 15)
                    db.bring(chat.id, 'Вишня', 'items', 20)
                    db.bring(chat.id, 'Земляника', 'items', 30)
                    db.bring(chat.id, 'Панцирь', 'hunter', 3)

                    db.add_item(chat.id, 'protection', 'potions', 1)

@dp.callback_query_handler(text='health')
async def potion(call : CallbackQuery):
    chat = call.message.chat
    msg = call.message
    if chat.id > 0:
        if not db.check(chat.id):
            await msg.answer(
                conf.read('non').format(
                    chat.id, chat.first_name
                ),
                reply_markup=menu.Main.markup
            )

            db.add_user(chat.id)
        else:
            if db.get(chat.id, 'users', 'lock')[0] == 'Лагерь':
                isc = [
                    '✅' if db.get(chat.id, 'items', 'Малина')[0]    >= 20 else '❌', 
                    '✅' if db.get(chat.id, 'items', 'Вишня')[0]     >= 20 else '❌', 
                    '✅' if db.get(chat.id, 'items', 'Земляника')[0] >= 20 else '❌', 
                    '✅' if db.get(chat.id, 'hunter', 'Мох')[0]      >= 3  else '❌', 
                ]

                if isc == ['✅','✅','✅','✅']:
                    try:
                        await msg.delete()
                    except Exception as e:
                        print(e)

                    await msg.answer(
                        'Вы успешно сварили зелье'
                    )

                    db.bring(chat.id, 'Малина', 'items', 20)
                    db.bring(chat.id, 'Вишня', 'items', 20)
                    db.bring(chat.id, 'Земляника', 'items', 20)
                    db.bring(chat.id, 'Мох', 'hunter', 3)

                    db.add_item(chat.id, 'health', 'potions', 1)

@dp.callback_query_handler(text='luck')
async def potion(call : CallbackQuery):
    chat = call.message.chat
    msg = call.message
    if chat.id > 0:
        if not db.check(chat.id):
            await msg.answer(
                conf.read('non').format(
                    chat.id, chat.first_name
                ),
                reply_markup=menu.Main.markup
            )

            db.add_user(chat.id)
        else:
            if db.get(chat.id, 'users', 'lock')[0] == 'Лагерь':
                isc = [
                    '✅' if db.get(chat.id, 'items', 'Малина')[0]    >= 50 else '❌', 
                    '✅' if db.get(chat.id, 'items', 'Вишня')[0]     >= 30 else '❌', 
                    '✅' if db.get(chat.id, 'items', 'Земляника')[0] >= 50 else '❌', 
                    '✅' if db.get(chat.id, 'hunter', 'Сгусток')[0]  >= 3  else '❌', 
                ]

                if isc == ['✅','✅','✅','✅']:
                    try:
                        await msg.delete()
                    except Exception as e:
                        print(e)

                    await msg.answer(
                        'Вы успешно сварили зелье'
                    )

                    db.bring(chat.id, 'Малина', 'items', 50)
                    db.bring(chat.id, 'Вишня', 'items', 30)
                    db.bring(chat.id, 'Земляника', 'items', 50)
                    db.bring(chat.id, 'Сгусток', 'hunter', 3)

                    db.add_item(chat.id, 'luck', 'potions', 1)

@dp.callback_query_handler(text='energy')
async def potion(call : CallbackQuery):
    chat = call.message.chat
    msg = call.message
    if chat.id > 0:
        if not db.check(chat.id):
            await msg.answer(
                conf.read('non').format(
                    chat.id, chat.first_name
                ),
                reply_markup=menu.Main.markup
            )

            db.add_user(chat.id)
        else:
            if db.get(chat.id, 'users', 'lock')[0] == 'Лагерь':
                isc = [
                    '✅' if db.get(chat.id, 'items', 'Малина')[0]    >= 20 else '❌', 
                    '✅' if db.get(chat.id, 'items', 'Вишня')[0]     >= 20 else '❌', 
                    '✅' if db.get(chat.id, 'items', 'Земляника')[0] >= 20 else '❌',
                ]

                if isc == ['✅','✅','✅']:
                    try:
                        await msg.delete()
                    except Exception as e:
                        print(e)

                    await msg.answer(
                        'Вы успешно сварили зелье'
                    )

                    db.bring(chat.id, 'Малина', 'items', 20)
                    db.bring(chat.id, 'Вишня', 'items', 20)
                    db.bring(chat.id, 'Земляника', 'items', 20)

                    db.add_item(chat.id, 'energy', 'potions', 1)


""" --------------------------------------------------- """

if __name__ == "__main__":
    try:
        executor.start_polling(
            dp, skip_updates=True
        )
    except Exception as e:
        print(e)
