#Autor: FIlip Drvoderić

import random

def roll_dice():
    return random.randint(1, 6)

def move_piece(position, roll):
    if position + roll > 30:
        return -1
    elif position + roll == 30:
        return 100
    return position + roll

def game_over(positions):
    return all(pos == 100 for pos in positions)

def initialize_pieces():
    return [-1, -1, -1, -1]

def can_move_out(roll):
    return roll == 6

def choose_piece_human(player_pieces, roll):
    print(f"Igračeve figure su na pozicijama: {player_pieces}")
    print(f"Bacili ste {roll}.")

    valid_moves_exist = valid_move_exists(player_pieces, roll)

    if not valid_moves_exist and roll != 6:
        print("Nema dostupnih poteza, preskačete potez.")
        return None

    print("Odaberite figuru koju želite pomaknuti (0-3) ili unesite -1 za preskakanje poteza:")
    while True:
        choice = int(input())
        if choice == -1:
            return None
        if choice in range(4):
            if player_pieces[choice] == -1:
                if roll != 6:
                    print("Niste bacili 6, ne možete postaviti novog čovječuljka na ploču.")
                    continue
                else:
                    return choice
            elif player_pieces[choice] != 100 and move_piece(player_pieces[choice], roll) != -1:
                return choice
        print("Niste odabrali ispravnu figuru ili potez, pokušajte ponovno!")



def choose_piece_ai_minimax(player_pieces, roll, opponent_pieces):
    best_move = None
    best_score = -float('inf')

    def captures_opponent(new_position):
        return new_position in opponent_pieces and new_position != 100

    for i, piece in enumerate(player_pieces):
        if piece == 100:
            continue

        new_position = move_piece(piece, roll)
        if new_position == -1:
            continue

        score = 0

        if piece == -1 and roll == 6:
            score = 1000
        elif new_position == 100:
            score = 900
        elif captures_opponent(new_position):
            score = 800
        else:
            score = new_position

        if score > best_score:
            best_score = score
            best_move = i

    return best_move

def capture_piece(players, current_player, new_position):
    other_player = 1 - current_player
    for i in range(4):
        if players[other_player][i] == new_position and new_position != 100:
            players[other_player][i] = -1
            break

def valid_move_exists(player_pieces, roll):
    return any(move_piece(piece, roll) != -1 for piece in player_pieces if piece != -1 and piece != 100)

def display_positions(players):
    print(f"Pozicije Igrača: {players[0]}")
    print(f"Pozicije AI protivnika: {players[1]}")

def print_board(players):
    board = [" " for _ in range(31)]
    for i, pos in enumerate(players[0]):
        if pos >= 0 and pos != 100:
            board[pos] = f"P{i + 1}"
    for i, pos in enumerate(players[1]):
        if pos >= 0 and pos != 100:
            board[pos] = f"A{i + 1}"
    board_str = "|" + "|".join(board) + "|"
    print(board_str)


player_pieces = initialize_pieces()
ai_pieces = initialize_pieces()
current_player = 0
players = [player_pieces, ai_pieces]

while True:
    roll = roll_dice()
    print(f"{['Igrač', 'AI protivnik'][current_player]} je bacio {roll}.")
    if can_move_out(roll):
        if current_player == 0:
            players[current_player][0] = 0
        break
    current_player = 1 - current_player

while not game_over(players[0]) and not game_over(players[1]):
    display_positions(players)
    print_board(players)
    roll = roll_dice()
    print(f"{['Igrač', 'AI protivnik'][current_player]} je na potezu i bacio je {roll}.")

    if current_player == 0:
        piece_index = choose_piece_human(players[current_player], roll)
    else:
        piece_index = choose_piece_ai_minimax(players[current_player], roll, players[1 - current_player])

    if piece_index is not None:
        if players[current_player][piece_index] == -1:
            players[current_player][piece_index] = 0
        else:
            new_position = move_piece(players[current_player][piece_index], roll)
            capture_piece(players, current_player, new_position)
            players[current_player][piece_index] = new_position

        print(f"{['Igrač', 'AI protivnik'][current_player]} pomaknuo figuru {piece_index} na poziciju {players[current_player][piece_index]}.")


    if roll != 6:
        current_player = 1 - current_player

winner = "Igrač" if game_over(players[0]) else "AI protivnik"
print(f"Igra je završila. Pobjednik je {winner}!")
