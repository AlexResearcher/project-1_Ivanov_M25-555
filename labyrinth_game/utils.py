#!/usr/bin/env python3
import math

from labyrinth_game.constants import ROOMS


def describe_current_room(game_state):
    '''
    Описание текущей команты
    '''
    room_name = game_state["current_room"]
    room_data = ROOMS.get(room_name)
    
    if room_data:
        print(f"\n\n== {room_name.upper()} ==")
        print(room_data["description"])
        
        items = room_data.get("items", [])
        if items:
            print("Заметные предметы:")
            for item in items:
                print("-", item)
                
        exits = room_data.get("exits", {})
        if exits:
            print("Выходы:", ", ".join(exits.keys()))
            
        puzzle = room_data.get("puzzle")
        if puzzle:
            print("Кажется, здесь есть загадка (используйте команду solve).")
    else:
        print("Ошибка: комната не найдена.")

def solve_puzzle(game_state):
    '''
    Оределяется факт решения или не решения головоломки. 
    Логика получения вознаграждения за решение головоломки
    '''
    current_room = game_state["current_room"]
    room_data = ROOMS[current_room]
    puzzle = room_data.get("puzzle")
    #если награда указана в словаре ROOMS
    reward = room_data.get("reward")

    if not puzzle:
        print("Загадок здесь нет.")
        return

    question, answers = puzzle
    print(question)
    user_answer = input("Ваш ответ: ")

    if user_answer.strip().lower() in answers:
        print("Правильно! Загадка решена.")
    #убираем головоломку, чтобы нельзя было решать дважды
        del room_data["puzzle"] 
        if not reward:
    #награда за разгадку, кроме тех случаев, где награда указана в словаре ROOMS
            reward = "coin" 
        game_state["player_inventory"].append(reward)
        print(f"Получено вознаграждение: {reward}.")
    elif current_room == "trap_room": #ответ неверный и trap_room
        trigger_trap(game_state)
    else:
        print("Неверно. Попробуйте снова.")
    
def attempt_open_treasure(game_state):
    '''
    Попытка открыть сундук с сокровищами и условия для его открытия
    '''
    current_room = game_state["current_room"]
    room_data = ROOMS[current_room]

    if "treasure_chest" not in room_data["items"]:
        print("Сундук уже открыт или отсутствует.")
        return

    keys_in_inventory = any(key in game_state["player_inventory"]\
                            for key in ["treasure_key", "rusty_key"])

    if keys_in_inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room_data["items"].remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
    else:
        response = input("Сундук заперт. Ввести код? (да/нет) ")
        if response.strip().lower() != "да":
            print("Вы отступаете от сундука.")
            return

        code_attempt = input("Введите код: ")
        puzzle = room_data.get("puzzle")
        if puzzle and code_attempt.strip().lower() == puzzle[1]:
            print("Прекрасно! Замок открылся.")
            room_data["items"].remove("treasure_chest")
            print("В сундуке сокровище! Вы победили!")
            game_state["game_over"] = True
        else:
            print("Неверный код. Попытайтесь снова.")

def pseudo_random(seed, modulo):
    '''
    Возвращает случайным образом сгенерированное число.
    Нужно для определения урона или потери предмета в ловушке 
    и для ф-ии случайного события
    '''
    #число для размазывания значений
    number1 = 12.9898  
    #число для увеличения разброса
    number2 = 43758.5453  
    #синус от seed, умноженного на число 1
    sin_value = math.sin(seed * number1) 
    #умножаем на число 2
    multiplied_value = sin_value * number2 
    #выделяем дробную часть
    part = multiplied_value - math.floor(multiplied_value) 
    #масштабируем дробную часть до диапазона [0, modulo)
    scaled_value = part * modulo 
    #округляем до ближайшего целого числа
    result = int(scaled_value)
    return result

def trigger_trap(game_state):
    '''
    Определяет урон или потерю предмета при попадании в ловушку
    '''
    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state.get("player_inventory", [])

    if inventory:
        #выбор случайного индекса предмета
        index = pseudo_random(game_state["steps_taken"], len(inventory)) 
        lost_item = inventory.pop(index)
        print(f"Потерян предмет: {lost_item}")
    else:
        #генератор случайного урона от 0 до 9
        damage = pseudo_random(game_state["steps_taken"], 10)  
        if damage <= 3:  #критический порог повреждения
            print("Вы получили смертельный удар! Игра закончена.")
            game_state["game_over"] = True
        else:
            print("Вы избежали смерти.")

def random_event(game_state):
    '''
    Определяет случайные события 
    '''
    #один из сценариев произойдет если выпадет число 5
    event_happens = pseudo_random(game_state["steps_taken"], 10) == 5  
    if not event_happens:
        return

    #три возможных сценария [0,1,2]
    scenario = pseudo_random(game_state["steps_taken"], 3)  

    if scenario == 0:
        print("Вы заметили блестящую монету на полу.")
        ROOMS[game_state["current_room"]]["items"].append("coin")
    elif scenario == 1:
        print("Вы услышали подозрительный шорох поблизости.")
        if "sword" in game_state["player_inventory"]:
            print("Вы отпугнули неизвестное существо своим мечом.")
    elif scenario == 2:
        if game_state["current_room"] == "trap_room"\
            and "torch" not in game_state["player_inventory"]:
            print("Темнота скрывает опасность. Вы чувствуете вибрацию пола.")
            trigger_trap(game_state)

def show_help(commands):
    print("Доступные команды:")
    for command, description in commands.items():
        print(f"{command:<16} - {description}")
