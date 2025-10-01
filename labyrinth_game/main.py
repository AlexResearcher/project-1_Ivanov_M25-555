#!/usr/bin/env python3

from labyrinth_game.utils import describe_current_room, attempt_open_treasure, solve_puzzle
from labyrinth_game.player_actions import get_input, take_item, move_player, show_inventory, use_item

def process_command(game_state, command):
        parts = command.split(maxsplit=1)
        action = parts[0]
        arg = parts[1] if len(parts) > 1 else None

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
            case _:
                print("Неизвестная команда.")

def main():
    game_state = {
        'player_inventory': [], # Инвентарь игрока
        'current_room': 'entrance', # Текущая комната
        'game_over': False, # Значения окончания игры
        'steps_taken': 0 # Количество шагов
  }
    # Приветственное сообщение
    print("Добро пожаловать в Лабиринт сокровищ!\n")

    # Описание начальной комнаты
    describe_current_room(game_state)

    # Основной игровой цикл
    while not game_state["game_over"]:
        command = get_input("> ")  # Вызов нашей функции get_input()
        if command == "quit":
            break
        process_command(game_state, command)

if __name__ == "__main__":
    main()