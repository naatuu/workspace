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


def change_turn(turn):  # 練習2
    if turn == BOARD_SENTE:
        return BOARD_GOTE
    elif turn == BOARD_GOTE:
        return BOARD_SENTE


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
        if board[row][col] == change_turn(turn):
            count += 1
        elif board[row][col] == turn:
            return count
        else:
            break
        row += row_inc
        col += col_inc
    return 0


def board_movable(board, row, col, turn):  # 練習5
    if board[row][col] != BOARD_EMPTY:
        return False
    for row_inc, col_inc in BOARD_DIRECTIONS:
        if board_scan(board, row, col, row_inc, col_inc, turn) > 0:
            return True
    return False


def board_movable_any(board, turn):  # 練習6
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board_movable(board, row, col, turn):
                return True
    return False


def board_move(board, row, col, turn):  # 練習7
    if not board_movable(board, row, col, turn):
        return False
    board[row][col] = turn
    for row_inc, col_inc in BOARD_DIRECTIONS:
        count = board_scan(board, row, col, row_inc, col_inc, turn)
        for i in range(1, count + 1):
            board[row + i * row_inc][col + i * col_inc] = turn
    return True


def board_number_check(board, turn):  # 練習8
    count = 0
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == turn:
                count += 1
    return count


def board_eval(board):  # 練習9
    count_sente = 0
    count_gote = 0

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == BOARD_SENTE:
                count_sente += 1
            elif board[row][col] == BOARD_GOTE:
                count_gote += 1

    denominator = count_sente + count_gote

    if denominator == 0:
        return 0.0

    numerator = count_sente - count_gote
    return numerator / denominator


def board_state(board, turn):  # 練習10
    if board_movable_any(board, turn):
        return None  # ゲーム継続中
    elif board_movable_any(board, change_turn(turn)):
        return "pass"  # パス
    else:
        return float(board_eval(board))  # 終局


def game_result(board, state):  # 練習11
    if state > 0:
        result = "Game Won by Sente"
    elif state < 0:
        result = "Game Won by Gote"
    else:
        result = "Draw"

    return f"{result}\nScore is {board_number_check(board, BOARD_SENTE)} - {board_number_check(board, BOARD_GOTE)}"


def play_by_human(board, turn, count):  # 練習12
    # 合法手がない場合は何も入力させずに戻る（呼び出し側でパス処理を行う）。
    if not board_movable_any(board, turn):
        return
    while True:
        # 入力が2つの整数でない場合は再入力させる。
        inp = input(f"({count}) Enter row and col for {BOARD_SYMBOL[turn]}: ")
        parts = inp.strip().split()
        if len(parts) != 2:
            continue
        try:
            row = int(parts[0]) - 1
            col = int(parts[1]) - 1
        except ValueError:
            continue
        # 盤面外、または合法手でない場合は再入力させる。
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            continue
        # 合法手であれば board_move() で盤面を更新して戻る。
        if board_move(board, row, col, turn):
            return


def othello(sente_gote, yomi_depth=None):  # 練習13
    pass


print_board(initial_board())
