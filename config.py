from dotenv import load_dotenv
from os     import getenv

load_dotenv()
db = getenv("DB")


class Settings:
    def __init__(self):
        self.token   = getenv("TOKEN")
        self.channel = getenv("CHANNEL")
        self.maker   = getenv("MAKER")
        self.isSend  = ""

        # локации
        self.locks = [
            "Лагерь", "Лес", "Монстры", "Озеро", "Шахта"
        ]

        # предметы из леса
        self.items = {
            'usual'  : ["Ветки", "Листья", "Камни"],
            'rare'   : ["Доски", "Вишня", "Малина", "Земляника", "Ткань"],
            'uprare' : ["Пластины", "Гайки", "Болты", "Шестеренки"]
        }

        # emoji
        self.emoji = {
            'Ветки':'🌿','Листья':'🍃','Камни':'🪨',
            'Доски':'🪵', 'Ткань':'🧶', 'Вишня':'🍒', 'Малина':'🍓','Земляника':'🫐',
            'Пластины':'📏','Гайки':'🔩', 'Болты':'🔩','Шестеренки':'⚙️',
            'Клык':'🦷','Панцирь':'🐢','Сгусток':'🧬','Мох':'🌱',

            'Слоновья ярость': '💪','Черепашья мощь': '🛡',
            'Асцидиева живучесть': '❤️','Удача Ямагучи': '🍀',

            'Железо':'📏',
            'Уголь':'◼️',
            'Алюминий':'📏',
            'Медь':'🥉',
            'Золото':'🥇',
            'Серебро' : '🥈'
        }

        # предметы из мобов
        self.mob_items = {
            'usual': "Шестеренки",
            'epic' : ["Клык", "Панцирь", "Сгусток", "Мох"],
        }

        # словарь мобов и предметов из них
        self.mobs = {
            'Клык'    : 'Слоновая крыса 🐘',
            'Панцирь' : 'Лев-черепаха 🐢',
            'Сгусток' : 'Мини-годзилла 🦖',
            'Мох'     : 'Древесная лягушка 🐸',
        }

        self.mine = {
            'usual'  : ["Железо", "Уголь"],
            'rare'   : ["Алюминий", "Медь"],
            'uprare' : ["Золото", "Серебро"],
        }

        self.price = {
            'Железо':0.04,
            'Уголь':0.01,
            'Алюминий':0.01,
            'Медь':0.01,
            'Золото':63.0,
            'Серебро':1.00,
        }

        self.weapon = {
            'Отсутствует'     : 0,
            'Деревянный меч'  : 50,
            'Бронзовый меч'   : 100,
            'Железный меч'    : 280,
            'Укрепленный меч' : 350
        }

        self.armor = {
            'Отсутствует'       : 0,
            'Кожаная броня'     : 50,
            'Бронзовая броня'   : 100,
            'Железная броня'    : 250,
            'Укрепленная броня' : 320
        }

        self.pick = {
            'Отсутствует'       : 5.0,
            'Деревянная кирка'  : 3.5,
            'Бронзовая кирка'   : 2.5,
            'Железная кирка'    : 2.0,
            'Укрепленная кирка' : 1.0,
        }

        self.row = {
            'Отсутствует'        : 5.0,
            'Деревянная удочка'  : 3.5,
            'Бронзовая удочка'   : 2.5,
            'Железная удочка'    : 2.0,
            'Укрепленная удочка' : 1.0,
        }


        self.all_items = {
            'items' : [
                'Ветки','Листья','Камни','Доски','Ткань','Вишня',
                'Малина','Земляника','Пластины','Гайки','Болты','Шестеренки'
            ],

            'potions' : [
                'Слоновья ярость','Черепашья мощь',
                'Асцидиева живучесть','Удача Ямагучи'
            ],
            
            'hunter' : ['Клык','Панцирь','Сгусток','Мох',],

            'mine' : ['Железо','Уголь','Алюминий','Медь','Золото','Серебро',],

            # 'weapon' : [
            #     'Деревянный меч',
            #     'Бронзовый меч',
            #     'Железный меч',
            #     'Укрепленный меч',
            # ],
            # 'armor' : [
            #     'Кожаная броня',
            #     'Бронзовая броня',
            #     'Железная броня',
            #     'Укрепленная броня',
            # ],
            # 'pick' : [
            #     'Деревянная кирка',
            #     'Бронзовая кирка',
            #     'Железная кирка',
            #     'Укрепленная кирка',
            # ],
            # 'row' : [
            #     'Деревянная удочка',
            #     'Бронзовая удочка',
            #     'Железная удочка',
            #     'Укрепленная удочка',
            # ]

        }

    def read(self, name:str):
        with open(f'msg/{name}.txt', 'r') as file:
            return str(file.read())