#!/usr/bin/env python3
from labyrinth_game.constants import COMMANDS
from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    show_help,
    solve_puzzle,
)


def process_command(game_state, command):
        '''
        Обработка команд игрока
        '''
        parts = command.split(maxsplit=1)
        action = parts[0]
        arg = parts[1] if len(parts) > 1 else None

        #обработка движений без go
        directions = ["north", "south", "east", "west"]
        if action in directions:
            move_player(game_state, action)
            return

        match action:
            case "look":
                describe_current_room(game_state)
            case "go":
                move_player(game_state, arg)
            case "take":
                take_item(game_state, arg)
            case "use":
                if arg == "treasure_chest":
                    attempt_open_treasure(game_state)
                else:
                    use_item(game_state, arg)
            case "inventory":
                show_inventory(game_state)
            case "quit" | "exit":
                print("До свидания!")
                game_state["game_over"] = True
            case "solve":
                if game_state["current_room"] == "treasure_room":
                    attempt_open_treasure(game_state)
                else:
                    solve_puzzle(game_state)
            case "help":
                show_help(COMMANDS)
            case _:
                print("Неизвестная команда.")

def main():
    game_state = {
        'player_inventory': [], #инвентарь игрока
        'current_room': 'entrance', #текущая комната
        'game_over': False, #значения окончания игры
        'steps_taken': 0 #количество шагов
  }
    print("Добро пожаловать в Лабиринт сокровищ!\n")

    #описание комнаты
    describe_current_room(game_state)

    #игровой цикл
    while not game_state["game_over"]:
        #вызов функции get_input() для обработки ввода команд
        command = get_input("> ")  
        if command == "quit":
            break
        process_command(game_state, command)

if __name__ == "__main__":
    main()