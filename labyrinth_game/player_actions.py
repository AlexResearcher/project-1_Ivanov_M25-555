#!/usr/bin/env python3
from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room, random_event


def show_inventory(game_state:dict):
    '''
    Показывает содержимое инветаря
    '''
    inventory = game_state.get("player_inventory", [])
    if inventory:
        print("Содержимое инвентаря:")
        for item in inventory:
            print("-", item)
    else:
        print("Инвентарь пуст.")

def get_input(prompt="> "):
    '''
    Обработка ввода игрока
    '''
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("Выход из игры.")
        return "quit"
    
def move_player(game_state, direction):
    '''
    Отвечает за переход игрока в новую комнату по его команде
    '''
    current_room = game_state["current_room"]
    exits = ROOMS[current_room]["exits"]
    random_event(game_state)
    if direction in exits:
        new_room = exits[direction]

        #проверка для комнаты сокровищ
        if new_room == "treasure_room":
            if "treasure_key" or "rusty_key" in game_state["player_inventory"]:
                print("Вы используете найденный ключ,\
 чтобы открыть путь в комнату сокровищ.")
                game_state["current_room"] = new_room
                game_state["steps_taken"] += 1
                describe_current_room(game_state)
            else:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")       
        else:
            game_state["current_room"] = new_room
            game_state["steps_taken"] += 1
            describe_current_room(game_state)
    else:
        print("Нельзя пойти в этом направлении.")

def take_item(game_state, item_name):
    '''
    Поднятие предметов
    '''
    current_room_items = ROOMS[game_state["current_room"]]["items"]

    if item_name in current_room_items:
        game_state["player_inventory"].append(item_name)
        current_room_items.remove(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state, item_name):
    '''
    Использование предметов
    '''
    if item_name not in game_state["player_inventory"]:
        print("У вас нет такого предмета.")
        return
    if item_name == "torch":
        print("Свет освещает помещение.")
    elif item_name == "sword":
        print("Вы ощущащете чувство уверенности.")
    elif item_name == "bronze_box":
        if "rusty_key" not in game_state["player_inventory"]:
            game_state["player_inventory"].append("rusty_key")
            print("Вы открыли шкатулку и взяли ключ.")
        else:
            print("Шкатулка уже открыта.")
    elif item_name == "paper_page":
        print("Код для открытия сундука без ключа: 10")
    else:
        print("Вы не знаете, как использовать этот предмет.")