import random
import datetime as dt

pos_per_line = 3    # line length of tic tac toe grid
board = [[" " for y in range(pos_per_line)] for x in range(pos_per_line)]


def show_board(bo):
    """text based visualization of playing field"""
    for x in range(pos_per_line):
        for y in range(pos_per_line):
            if y < pos_per_line-1:
                print(f" {bo[x][y]} |", end="")
            else:
                print(f" {bo[x][y]} ")
        if x < pos_per_line-1:
            for _ in range(pos_per_line-1):
                print("———|", end="")
            print("———")


def pos_available(coor: [tuple]):
    return board[coor[0]][coor[1]] == " "


def winning_const(bo):
    """checks the board for winning lines and if found, returns winning letter"""
    # lines and columns
    for x in range(pos_per_line):
        l_lst = []
        for y in range(pos_per_line):
            l_lst.append(bo[x][y])      # list of lines
        if len(set(l_lst)) == 1 and set(l_lst) != {" "}:
            return set(l_lst).pop()
    for y in range(pos_per_line):
        c_lst = []
        for x in range(pos_per_line):
            c_lst.append(bo[x][y])  # list of cols
        if len(set(c_lst)) == 1 and set(c_lst) != {" "}:
            return set(c_lst).pop()
    # diagonals
    top_left = []       # start top left (goes to bottom right)
    top_right = []      # start top right (goes to bottom left)
    for d in range(pos_per_line):
        top_left. append(bo[d][d])
        top_right.append(bo[d][pos_per_line-d-1])
    if len(set(top_left)) == 1 and set(top_left) != {" "}:
        return set(top_left).pop()
    if len(set(top_right)) == 1 and set(top_right) != {" "}:
        return set(top_right).pop()
    return None


def position_to_coords(pos: [int] = 0):
    y = pos
    while y > pos_per_line:
        y -= pos_per_line
    if pos % pos_per_line != 0:
        x = pos // pos_per_line
    else:
        x = pos // pos_per_line - 1
    return x, y-1


def no_more_empty(bo):
    for _ in range(pos_per_line):
        if " " in bo[_]:
            return False
    return True


def list_empty_fields(bo):
    empty_list = []
    for x in range(pos_per_line):
        for y in range(pos_per_line):
            if bo[x][y] == " ":
                empty_list.append((x, y))
    return empty_list


def check_line_empty(line_num: [int], axis: [int]):
    """axis = 0 means horizontal, axis = 1 means vertical"""
    global board
    line_lst = []
    if axis == 0:
        for p in range(pos_per_line):
            line_lst.append(board[line_num][p])
        return set(line_lst) == {" "}
    if axis == 1:
        for p in range(pos_per_line):
            line_lst.append(board[p][line_num])
        return set(line_lst) == {" "}


def computer_move(letter: [str] = "O"):
    global board
    possible_moves = list_empty_fields(board)
    board_copy = board[:]   # new board to check for placements without affecting the original board

    # check for possible winning moves possible for computer -> if found, place O in original board and return
    for p in possible_moves:
        board_copy[p[0]][p[1]] = letter
        if winning_const(board_copy):
            board[p[0]][p[1]] = letter      # -> winning move placed
            return
        else:
            board_copy[p[0]][p[1]] = " "    # -> replace the letter with blank and continue with loop

    # check for possible winning moves possible for player -> if found, place O in original board and return
    opposite_letter = "X" if letter == "O" else "O"
    for p in possible_moves:
        board_copy[p[0]][p[1]] = opposite_letter
        if winning_const(board_copy):
            board[p[0]][p[1]] = letter      # -> possible winning move by player blocked
            return
        else:
            board_copy[p[0]][p[1]] = " "    # -> replace the letter with blank and continue with loop

    # take center if available
    if board[pos_per_line//2][pos_per_line//2] == " ":
        board[pos_per_line//2][pos_per_line//2] = letter
        return

    # take top horizontal line, if still completely empty
    elif check_line_empty(0, 0):
        if not check_line_empty(0, 1):      # take the corner in the same vertical line as player choice
            board[0][0] = letter
        else:
            board[0][pos_per_line - 1] = letter
        return
    # take bottom horizontal line, if still completely empty
    elif check_line_empty(pos_per_line-1, 0):
        if not check_line_empty(pos_per_line-1, 1):  # take the corner in the same vertical line as player choice
            board[pos_per_line-1][pos_per_line-1] = letter
        else:
            board[pos_per_line-1][0] = letter
        return

    # take left vertical line, if still completely empty
    elif check_line_empty(0, 1):
        board[random.choice([0, pos_per_line - 1])][0] = letter
        return
    # take right vertical line, if still completely empty
    elif check_line_empty(pos_per_line-1, 1):
        board[random.choice([0, pos_per_line-1])][pos_per_line-1] = letter
        return

    # take an empty corner, if available
    elif board[0][0] == " ":
        board[0][0] = letter
        return
    elif board[0][pos_per_line - 1] == " ":
        board[0][pos_per_line - 1] = letter
        return
    elif board[pos_per_line - 1][0] == " ":
        board[pos_per_line - 1][0] = letter
        return
    elif board[pos_per_line - 1][pos_per_line - 1] == " ":
        board[pos_per_line - 1][pos_per_line - 1] = letter
        return

    # take any random empty field
    else:
        random_field = random.randint(0, len(possible_moves)-1)
        board[possible_moves[random_field][0]][possible_moves[random_field][1]] = letter
        return


def player_move():
    global board
    not_valid = True
    while not_valid:
        try:
            move = int(input(f"Choose position (1 to {pos_per_line ** 2}): "))
        except ValueError:
            print("Invalid choice.")
            continue
        else:
            if move > pos_per_line**2:
                print("Invalid choice.")
                continue
            coords = position_to_coords(int(move))
            if pos_available(coords):
                board[coords[0]][coords[1]] = "X"
                not_valid = False
            else:
                print("Position not available, please choose again.")


def computer_vs_computer():
    """test function, runs through all possible starting positions of a grid, prints in the end the outcome: games
    played, wins and ties (uncomment no_tie and while loop for endless runs)"""
    global board
    start_time = dt.datetime.now()
    print(f"Running {pos_per_line**2} starting positions for the {pos_per_line} by {pos_per_line} tic tac toe grid.\n")
    game_counter = 0
    xes = 0
    oes = 0
    ties = 0
    # no_tie = False
    # while no_tie:
    for plays in range(pos_per_line ** 2):
        game_counter += 1
        (x, y) = position_to_coords(plays+1)
        board = [[" " for y in range(pos_per_line)] for x in range(pos_per_line)]
        board[x][y] = "X"
        # board[random.randint(1, pos_per_line)][random.randint(1, pos_per_line)] = "X"  # uncomment in infinite run
        # show_board(board)
        for _ in range(pos_per_line**2-1):
            computer_move("X")
            if winning_const(board):
                print("**********************************")
                print(f"* The Game is over, the {winning_const(board)}'s won. *")
                print("**********************************")
                if winning_const(board) == "X":
                    xes += 1
                elif winning_const(board) == "O":
                    oes += 1
                # no_tie = False
                break
            if no_more_empty(board):
                # print("\n ~ ~ ~ ~ ~ ~ ~ ~ ~ ~\nThis Game is a tie.\n ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")
                show_board(board)
                break

            computer_move("O")
            if winning_const(board):
                print("**********************************")
                print(f"* The Game is over, the {winning_const(board)}'s won. *")
                print("**********************************")
                # no_tie = False
                break
            if no_more_empty(board):
                # print("\n ~ ~ ~ ~ ~ ~ ~ ~ ~ ~\nThis Game is a tie.\n ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")
                ties += 1
                break
        if game_counter % 50 != 0:
            print(".", end="")
        else:
            print(".")
    end_time = dt.datetime.now()
    print(f"\n\nGames played: {game_counter}, X's won -> {xes}, O's won -> {oes}, game tied -> {ties}\n"
          f"Time taken = {str(end_time - start_time)}")


def game_on():
    global board
    starter = input("\nThe X's will be played by the (probably human) player, the O's will be used by the computer.\n"
                    "Who shall start? (H uman / C omputer) ")
    # player = None
    if starter.lower() != "h":
        plays = 2
        board[1][1] = "O"
        corr = 1        # move counter correction
        show_board(board)
    else:
        plays = 0
        corr = 0        # move counter correction
    next_move = True
    while next_move:
        if plays > 0:
            print(f"Placement number {plays-corr}\n——————————————————\n")
        if plays % 2 == 0:
            player_move()
            plays += 1
        else:
            computer_move()
            plays += 1
        if winning_const(board):
            print("**********************************")
            print(f"* The Game is over, the {winning_const(board)}'s won. *")
            print("**********************************")
            next_move = False
            break
        if no_more_empty(board):
            print("\n ~ ~ ~ ~ ~ ~ ~ ~ ~ ~\nThis Game is a tie.\n ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")
            next_move = False
            break
        if next_move:
            show_board(board)
    show_board(board)
    print("\n\n")
    print(" ***************")
    print(" * TIC TAC TOE *")
    print(" ***************")


if __name__ == "__main__":
    # computer_vs_computer()
    print(" ***************")
    print(" * TIC TAC TOE *")
    print(" ***************")
    play = True
    while play:
        board = [[" " for y in range(pos_per_line)] for x in range(pos_per_line)]
        new_game = "r"
        while new_game.lower() not in ["y", "n"]:
            new_game = input("\nStart a new game (y/n)? ")
        if new_game.lower() == "y":
            game_on()
        else:
            play = False
            print("\nBye.")
