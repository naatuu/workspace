BOARD_SIZE = 8  # 盤上のサイズ
BOARD_SENTE = 1  # 先手
BOARD_GOTE = -1  # 後手
BOARD_EMPTY = 0  # 空き

BOARD_SENTE_STR = "*"  # 先手
BOARD_GOTE_STR = "o"  # 後手
BOARD_EMPTY_STR = "-"  # 空き

BOARD_SYMBOL = {
    BOARD_SENTE: BOARD_SENTE_STR,
    BOARD_GOTE: BOARD_GOTE_STR,
    BOARD_EMPTY: BOARD_EMPTY_STR,
}

BOARD_DIRECTIONS = [
    (0, 1),  # 右
    (1, 1),  # 右下
    (1, 0),  # 下
    (1, -1),  # 左下
    (0, -1),  # 左
    (-1, -1),  # 左上
    (-1, 0),  # 上
    (-1, 1),  # 右上
]


def initial_board():  # 練習1
    board = [[BOARD_EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    board[3][3] = BOARD_GOTE
    board[4][4] = BOARD_GOTE
    board[3][4] = BOARD_SENTE
    board[4][3] = BOARD_SENTE
    return board


def change_turn():  # 練習2
    return -turn


def print_board(board):  # 練習3
    print("R/C 1 2 3 4 5 6 7 8")
    for row in range(BOARD_SIZE):
        print(f"  {row + 1}", end=" ")
        for col in range(BOARD_SIZE):
            print(BOARD_SYMBOL[board[row][col]], end=" ")
        print()


def print_current_turn(turn):
    if turn == BOARD_SENTE:
        print("先手の番です。")
    elif turn == BOARD_GOTE:
        print("後手の番です。")
    else:
        print("無効なターンです。")


def board_scan(board, row0, col0, row_inc, col_inc, turn):  # 練習4
    row = row0 + row_inc
    col = col0 + col_inc
    count = 0
    while 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
        if board[row][col] == -turn:
            count += 1
        elif board[row][col] == turn:
            return count
        else:
            break
        row += row_inc
        col += col_inc
    return 0


def board_movable(board, row, col, turn):  # 練習5
    pass


def board_movable_any(board, turn):  # 練習6
    pass


def board_move(board, row, col, turn):  # 練習7
    pass


def board_number_check(board, turn):  # 練習8
    pass


def board_eval(board):  # 練習9
    pass


def board_state(board, turn):  # 練習10
    pass


def game_result(board, state):  # 練習11
    pass


def play_by_human(board, turn, count):  # 練習12
    pass


def othello(sente_gote, yomi_depth=None):  # 練習13
    pass


print_board(initial_board())
