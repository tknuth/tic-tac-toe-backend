from .core import *
import os
import time


def clear_output():
    os.system("clear")


def play_without_ai():
    bx = set()
    bo = set()

    while not is_over(bx, bo):
        clear_output()
        print_textboard(bx, bo)
        print()

        try:
            i = int(input(f"Auf welchem Feld möchtest du ein {turn(bx, bo)} setzen? "))
            assert i in range(9)
        except:
            print("Spiel abgebrochen.")
            return

        bx, bo = add_move(bx, bo, i)

    clear_output()
    print_textboard(bx, bo, placeholder=" ")
    print()

    if get_winner(bx, bo) is not None:
        print(f"{get_winner(bx, bo)} gewinnt!")
    else:
        print("Unentschieden!")
    time.sleep(3)


def input_move(bx, bo):
    return int(input(f"Auf welchem Feld möchtest du ein {turn(bx, bo)} setzen? "))


def play_with_ai():
    bx = set()
    bo = set()
    player_turn = True

    while not is_over(bx, bo):
        clear_output()
        print_textboard(bx, bo)
        print()

        if player_turn:
            try:
                i = input_move(bx, bo)
                assert i in range(9)
                cx, co = add_move(bx, bo, i)
                if bx != cx or bo != co:
                    player_turn = False
                bx, bo = cx, co
            except:
                print("Spiel abgebrochen.")
                return
        else:
            print("KI denkt ...")
            i = choose_move(bx, bo)
            time.sleep(1)
            bx, bo = add_move(bx, bo, i)
            player_turn = True

    clear_output()
    print_textboard(bx, bo, placeholder=" ")
    print()

    if get_winner(bx, bo) is not None:
        print(f"{get_winner(bx, bo)} gewinnt!")
    else:
        print("Unentschieden!")
    time.sleep(3)
