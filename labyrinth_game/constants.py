# labyrinth_game/constants.py
ROOMS = {
    'entrance': {
        'description': 'Вы в темном входе лабиринта...',
        'exits': {'north': 'hall', 'east': 'trap_room'},
        'items': ['torch'],
        'puzzle': None
    },
    'hall': {
        'description': 'Большой зал с эхом. По центру стоит пьедестал с запечатанным сундуком.',
        'exits': {'south': 'entrance', 'west': 'library', 'east':'coffee_room', 'north': 'treasure_room'},
        'items': [],
        'puzzle': ('На пьедестале надпись: "Назовите число, которое идет после девяти". Введите ответ цифрой или словом.', '10')
    },
    'trap_room': {
          'description': 'Комната с хитрой плиточной поломкой. На стене видна надпись: "Осторожно — ловушка".',
          'exits': {'west': 'entrance'},
          'items': ['rusty_key'],
          'puzzle': ('Система плит активна. Чтобы пройти, назовите слово "шаг" три раза подряд (введите "шаг шаг шаг")', 'шаг шаг шаг')
    },
    'library': {
          'description': 'Пыльная библиотека. На полках старые свитки. Где-то здесь может быть ключ от сокровищницы.',
          'exits': {'east': 'hall', 'north': 'armory'},
          'items': ['ancient_book'],
          'puzzle': ('В одном свитке вопрос: "Назовите год основания Руси?" (ответ одна цифра).', '862')
    },
        'armory': {
          'description': 'Старая оружейная комната. На стене висит меч, рядом — небольшая бронзовая шкатулка.',
          'exits': {'south': 'library'},
          'items': ['sword', 'bronze_box'],
          'puzzle': None
    },
    'treasure_room': {
          'description': 'Комната, на столе большой сундук. Дверь заперта — нужен особый ключ.',
          'exits': {'south': 'hall', 'east':'cabinet_room'},
          'items': ['treasure_chest'],
          'puzzle': ('Дверь защищена кодом. Введите код (подсказка: это число пятикратного шага, 2*5= ? )', '10')
    },
    'coffee_room': {
          'description': 'Кофейная комната. В середине комнаты стоит диван с кофейным столиком. На столе свежая чашка кофе для восстановления сил.',
          'exits': {'west': 'hall', 'south': 'cabinet_room'},
          'items': ['coffee_cup'],
          'puzzle': ('Загадка: Солнце с брызгами играет, Семь цветных полос включает.','радуга')
    }, 
    'cabinet_room': {
          'description':'Комната, у стены стоит стол, на столе лист бумаги. На нем написан код для открытия сундука с сокровищами.\
            Код: 10',    
          'exits': {'south': 'coffee_room', 'west':'treasure_room'},
          'items': ['paper_page'],
          'puzzle': None
    }
}