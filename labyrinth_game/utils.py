#!/usr/bin/env python3

from labyrinth_game.constants import ROOMS

def describe_current_room(game_state):
    room_name = game_state["current_room"]
    room_data = ROOMS.get(room_name)
    
    if room_data:
        print(f"== {room_name.upper()} ==")
        print(room_data["description"])
        
        items = room_data.get("items", [])
        if items:
            print("\nЗаметные предметы:")
            for item in items:
                print("-", item)
                
        exits = room_data.get("exits", {})
        if exits:
            print("\nВыходы:", ", ".join(exits.keys()))
            
        puzzle = room_data.get("puzzle")
        if puzzle:
            print("\nКажется, здесь есть загадка (используйте команду solve).")
    else:
        print("Ошибка: комната не найдена.")

def solve_puzzle(game_state):
    current_room = game_state["current_room"]
    room_data = ROOMS[current_room]
    puzzle = room_data.get("puzzle")

    if not puzzle:
        print("Загадок здесь нет.")
        return

    question, answer = puzzle
    print(question)
    user_answer = input("Ваш ответ: ")

    if user_answer.strip().lower() == answer.lower():
        print("Правильно! Загадка решена.")
        del room_data["puzzle"]  # Убираем головоломку, чтобы нельзя было решать дважды
        reward = "coin"  # Награда за разгадку
        game_state["player_inventory"].append(reward)
        print(f"Получено вознаграждение: {reward}.")
    else:
        print("Неверно. Попробуйте снова.")
    
def attempt_open_treasure(game_state):
    current_room = game_state["current_room"]
    room_data = ROOMS[current_room]

    if "treasure_chest" not in room_data["items"]:
        print("Сундук уже открыт или отсутствует.")
        return

    keys_in_inventory = any(key in game_state["player_inventory"] for key in ["treasure_key", "rusty_key"])

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