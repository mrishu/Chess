import os

ch = [['  '] * 8 for i in range(8)]


def init():
    
    ch[0][0] = 'R '
    ch[0][1] = 'N '
    ch[0][2] = 'B '
    ch[0][3] = 'Q '
    ch[0][4] = 'K '
    ch[0][5] = 'B '
    ch[0][6] = 'N '
    ch[0][7] = 'R '
    for i in range(8):
        ch[1][i] = 'P '

    ch[7][0] = 'r '
    ch[7][1] = 'n '
    ch[7][2] = 'b '
    ch[7][3] = 'q '
    ch[7][4] = 'k '
    ch[7][5] = 'b '
    ch[7][6] = 'n '
    ch[7][7] = 'r '
    for i in range(8):
        ch[6][i] = 'p '


init()

"""An important note must be made that 'P '.isupper() or 'p '.islower() would give True.
    This would be true for any letter other than 'p' or 'P'.
    Whereas, '  ', '* ' would give False for both islower() and isupper() methods."""


def disp(turn_to_play):
    os.system('cls')
    print("  +" + "-----+" * 8)
    if turn_to_play == 'w':
        for i in range(7, -1, -1):
            print(i + 1, "| ", str(ch[i]).lstrip("['").rstrip("]'").replace("', '", " |  "), "|")
            print("  |" + "     |" * 8)
            print("  +" + "-----+" * 8)
        print("     a     b     c     d     e     f     g     h")

    elif turn_to_play == 'b':
        for i in range(8):
            print(i + 1, "| ", str(ch[i][-1::-1]).lstrip("['").rstrip("]'").replace("', '", " |  "), "|")
            print("  |" + "     |" * 8)
            print("  +" + "-----+" * 8)
        print("     h     g     f     e     d     c     b     a")


def c(x, y):
    """Returns 1 if x < y and -1 if x > y."""
    return (y - x) // abs(y - x)


def move(ini, fin):
    ch[fin[0]][fin[1]] = ch[ini[0]][ini[1]]
    ch[ini[0]][ini[1]] = '  '


def add_stars(positions):
    for pos in positions:
        ch[pos[0]][pos[1]] = '*' + ch[pos[0]][pos[1]][0]


def remove_stars(positions):
    for pos in positions:
        ch[pos[0]][pos[1]] = ch[pos[0]][pos[1]][1] + " "


def empty(piece):
    """To check if given piece is empty
    Necessary because an empty position can be both '  ' or '* ' """
    if piece == '  ' or piece == '* ':
        return True
    return False


def on_attack(ini, fin):
    """To check if position at fin is under attack by piece by ini. If fin is under attack does not mean that the piece
    at ini can move over to fin since doing that can put a check on it's own king. This is checked in the
    legal(ini, fin) function."""
    
    global ep_pos

    i_piece = ch[ini[0]][ini[1]]  # Piece at ini
    f_piece = ch[fin[0]][fin[1]]  # Piece at fin

    # Try to get the en-passant activated pawn if there is no IndexError given by default position (9, 9).
    try:
        ep_pawn = ch[ep_pos[0]][ep_pos[1]]
    except IndexError:
        ep_pawn = "  "

    # Initial and Final Positions should not be same
    if ini == fin:
        return False

    # Condition that a piece cannot attack it's own team member
    if (i_piece.isupper() and f_piece.isupper()) or (i_piece.islower() and f_piece.islower()):
        return False

    # Condition for Pawns
    if i_piece == 'P ':
        if (fin[0] == ini[0] + 1 and fin[1] == ini[1] and empty(f_piece)) or (
                fin[0] == ini[0] + 1 and abs(fin[1] - ini[1]) == 1 and not empty(f_piece)) or (
                abs(ini[1] - ep_pos[1]) == 1 and ini[0] == ep_pos[0] and fin[0] == ini[0] + 1 and fin[1] == ep_pos[1] and ep_pawn.islower()) or(
                ini[0] == 1 and fin[0] == 3 and ini[1] == fin[1] and empty(ch[2][ini[1]]) and empty(f_piece)):
            return True
        else:
            return False

    elif i_piece == 'p ':
        if (fin[0] == ini[0] - 1 and fin[1] == ini[1] and empty(f_piece)) or (
                fin[0] == ini[0] - 1 and abs(fin[1] - ini[1]) == 1 and not empty(f_piece)) or(
                abs(ini[1] - ep_pos[1]) == 1 and ini[0] == ep_pos[0] and fin[0] == ini[0] - 1 and fin[1] == ep_pos[1] and ep_pawn.isupper()) or(
                ini[0] == 6 and fin[0] == 4 and ini[1] == fin[1] and empty(ch[5][ini[1]]) and empty(f_piece)):
            return True
        else:
            return False

    # Condition for Rooks
    elif i_piece == 'r ' or i_piece == 'R ':
        if ini[0] == fin[0]:
            for i in range(ini[1] + c(ini[1], fin[1]), fin[1], c(ini[1], fin[1])):
                if not empty(ch[ini[0]][i]):
                    return False
            return True

        elif ini[1] == fin[1]:
            for i in range(ini[0] + c(ini[0], fin[0]), fin[0], c(ini[0], fin[0])):
                if not empty(ch[i][ini[1]]):
                    return False
            return True
        else:
            return False

    # Condition for Bishops
    elif i_piece == 'b ' or i_piece == 'B ':
        if abs(fin[0] - ini[0]) == abs(fin[1] - ini[1]):
            i_increment = c(ini[0], fin[0])
            j_increment = c(ini[1], fin[1])
            i = ini[0] + i_increment
            j = ini[1] + j_increment
            while i != fin[0]:
                if not empty(ch[i][j]):
                    return False
                i += i_increment
                j += j_increment
            return True
        else:
            return False

    # Conditions for Queens
    # Either one of Rook or Bishop Conditions should be satisfied
    elif i_piece == 'q ' or i_piece == 'Q ':
        # Condition for Rook
        ch[ini[0]][ini[1]] = 'r ' if i_piece == 'q ' else 'R '
        legal1 = on_attack(ini, fin)

        # Condition for Bishop
        ch[ini[0]][ini[1]] = 'b ' if ch[ini[0]][ini[1]] == 'r ' else 'B '
        legal2 = on_attack(ini, fin)

        # Convert the piece back to normal
        ch[ini[0]][ini[1]] = 'q ' if ch[ini[0]][ini[1]] == 'b ' else 'Q '

        return legal1 or legal2

    # Condition for Knights
    elif i_piece == 'n ' or i_piece == 'N ':
        if (abs(fin[0] - ini[0]) == 2 and abs(fin[1] - ini[1]) == 1) or (
                abs(fin[0] - ini[0]) == 1 and abs(fin[1] - ini[1]) == 2):
            return True
        else:
            return False

    # Condition for Kings
    elif i_piece == 'k ' or i_piece == 'K ':
        if abs(fin[1] - ini[1]) <= 1 and abs(fin[0] - ini[0]) <= 1:
            return True
        else:
            return False


def is_forbid_king(k_piece):
    """Given the king, the function returns if that king is under check or not"""
    for i in range(8):
        for j in range(8):
            if ch[i][j] == k_piece:
                pos_king = i, j
                break
    for i in range(8):
        for j in range(8):
            if ch[i][j].isupper() and k_piece.islower() or ch[i][j].islower() and k_piece.isupper():
                if on_attack((i, j), pos_king):
                    return True
    return False


def legal(ini, fin):
    """If position at fin is under attack by piece at ini, this function checks whether moving the piece at ini to fin
    is legal or not. It might not be legal because moving there would put it's own king under check."""
    """To check that, we move the piece at ini to fin without displaying and check whether that configuration puts
    the piece's king under check."""
    
    if not on_attack(ini, fin):
        return False
    piece_at_fin = ch[fin[0]][fin[1]]
    move(ini, fin)
    if ch[fin[0]][fin[1]].islower() and is_forbid_king('k '):
        move(fin, ini)
        ch[fin[0]][fin[1]] = piece_at_fin
        return False
    if ch[fin[0]][fin[1]].isupper() and is_forbid_king('K '):
        move(fin, ini)
        ch[fin[0]][fin[1]] = piece_at_fin
        return False
        
    move(fin, ini)
    ch[fin[0]][fin[1]] = piece_at_fin
    return True


def possible_moves(ini):
    """Gives all the legal movable positions of the piece at ini."""
    possible_mov = []
    for i in range(8):
        for j in range(8):
            if legal(ini, (i, j)):
                possible_mov.append((i, j))
    return possible_mov


def input_valid(inp):
    if len(inp) != 2 or (inp[0] not in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']) or (
            inp[1] not in ['1', '2', '3', '4', '5', '6', '7', '8']):
        return False
    return True


def under_check_func():
    """To check whether a check was put under check in the previous turn."""
    global turn
    if is_forbid_king('k ') and turn == 'b':
        return True
    elif is_forbid_king('K ') and turn == 'w':
        return True
    return False


def legalmov_left_func():
    """To check if any legal move is left of the one in turn."""
    global turn
    if turn == 'b':
        for i in range(8):
            for j in range(8):
                if ch[i][j].islower() and possible_moves((i, j)) != []:
                    return True
    elif turn == 'w':
        for i in range(8):
            for j in range(8):
                if ch[i][j].isupper() and possible_moves((i, j)) != []:
                    return True
    return False


turn = 'w'
ep_pos = (9, 9)
"""ep_pos will give the position of en-passant activated pawn. (9, 9) index means no pawn is activated.
ch[9][9] would give IndexError but it is not at distance 1 from any column on chess board which is what we have used
in the on_attack() function."""

while True:
    disp(turn)

    under_check = under_check_func()
    legalmov_left = legalmov_left_func()

    if not legalmov_left and not under_check:
        print("\nStalemate. Draw.")
        input()
        break

    if under_check:
        if turn == 'b':
            if not legalmov_left:
                print("\nCheckmate. White Wins.")
                input()
                break
            else:
                print("\nBlack is under check.")
                input()
        else:
            if not legalmov_left:
                print("\nCheckmate. Black wins.")
                input()
                break
            else:
                print("\nWhite is under check.")
                input()

    # ini_pos_chs_conv is the position in chess convention, like a5, b6, c7 etc. Similarly for fin_pos_chs_conv.
    ini_pos_chs_conv = input("\nEnter initial position: ")

    if not input_valid(ini_pos_chs_conv):
        print("\nIllegal entry.")
        input()
        continue

    # ini_pos and fin_pos denote positions in cartesian form. For e.g ini('c7') or fin('c7') = (6,3)
    ini_pos = int(ini_pos_chs_conv[1]) - 1, ord(ini_pos_chs_conv[0]) - 97

    # The below if condition checks for:
    # There is no turn violation.
    # An empty place is not selected by using that: '  '.isupper() and '  '.islower() both are False
    if (turn == 'w' and ch[ini_pos[0]][ini_pos[1]].islower()) or (
            turn == 'b' and ch[ini_pos[0]][ini_pos[1]].isupper()) or (
            not ch[ini_pos[0]][ini_pos[1]].isupper() and not ch[ini_pos[0]][ini_pos[1]].islower()) or (
            empty(ch[ini_pos[0]][ini_pos[1]])):
        print("\nIllegal entry.")
        input()
        continue

    legal_positions = possible_moves(ini_pos)

    if not legal_positions:
        print("\nNo possible moves for this piece currently.")
        input()
        continue

    add_stars(legal_positions)
    disp(turn)

    fin_pos_chs_conv = input("\nEnter final position: ")

    if not input_valid(fin_pos_chs_conv):
        print("\nIllegal entry.")
        input()
        remove_stars(legal_positions)
        continue

    fin_pos = int(fin_pos_chs_conv[1]) - 1, ord(fin_pos_chs_conv[0]) - 97
    remove_stars(legal_positions)

    if fin_pos in legal_positions:

        # Activating a pawn for en-passant or resetting the en-passant position
        if (ch[ini_pos[0]][ini_pos[1]] == 'p ') or (ch[ini_pos[0]][ini_pos[1]] == 'P '):

            # Activating a new pawn for en-passant
            if abs(fin_pos[0] - ini_pos[0]) == 2:
                ep_pos = fin_pos

            # If the opponent uses en-passant on the en-passant activated pawn
            elif abs(fin_pos[0] - ini_pos[0]) == 1 and abs(fin_pos[1] - ini_pos[1]) == 1 and empty(ch[fin_pos[0]][fin_pos[1]]):
                ch[ep_pos[0]][ep_pos[1]] = "  "
                ep_pos = (9, 9)

        else:
            # If a new pawn is not activated for en-passant or en-passant is not used, reset the en-passant position
            ep_pos = (9, 9)

        # Pawn evolution
        if (ch[ini_pos[0]][ini_pos[1]] == 'p ' and fin_pos[0] == 0) or (
                ch[ini_pos[0]][ini_pos[1]] == 'P ' and fin_pos[0] == 7):
            new_piece = input("\nEnter the piece you want to evolve into: ")
            while new_piece not in ['q', 'r', 'b', 'n', 'Q', 'R', 'B', 'N']:
                print("\nInvalid choice.")
                input()
                disp(turn)
                new_piece = input("\nEnter the piece you want to evolve into: ")

            if fin_pos[0] == 0:
                ch[ini_pos[0]][ini_pos[1]] = new_piece.lower() + " "
            elif fin_pos[0] == 1:
                ch[ini_pos[0]][ini_pos[1]] = new_piece.upper() + " "

        move(ini_pos, fin_pos)

    else:
        print("\nEnter legal move.")
        input()
        remove_stars(legal_positions)
        continue

    if turn == 'w':
        turn = 'b'
    elif turn == 'b':
        turn = 'w'

# TODO:
# Add castling option
