import math
import random
import time
import matplotlib.pyplot as plt

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

NODE_CHECK_COUNT = 0

BOARD_POINT = [
    [30, -12, 0.1, -0.9, -0.9, 0.1, -12, 30],
    [-12, -15, -3, -3, -3, -3, -15, -12],
    [0.1, -3, 0, -1, -1, 0, -3, 0.1],
    [-0.9, -3, -1, -1, -1, -1, -3, -0.9],
    [-0.9, -3, -1, -1, -1, -1, -3, -0.9],
    [0.1, -3, 0, -1, -1, 0, -3, 0.1],
    [-12, -15, -3, -3, -3, -3, -15, -12],
    [30, -12, 0.1, -0.9, -0.9, 0.1, -12, 30],
]


def initial_board():  # 練習1_初期盤面
    board = [[BOARD_EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    board[3][3] = BOARD_GOTE
    board[4][4] = BOARD_GOTE
    board[3][4] = BOARD_SENTE
    board[4][3] = BOARD_SENTE
    return board


def change_turn(turn):  # 練習2_手番交代
    if turn == BOARD_SENTE:
        return BOARD_GOTE
    elif turn == BOARD_GOTE:
        return BOARD_SENTE


def print_board(board):  # 練習3_盤面表示
    print("R/C 1 2 3 4 5 6 7 8")
    for row in range(BOARD_SIZE):
        print(f"  {row + 1}", end=" ")
        for col in range(BOARD_SIZE):
            print(BOARD_SYMBOL[board[row][col]], end=" ")
        print()


def print_current_turn(turn):  # 練習3_現在の手番表示
    if turn == BOARD_SENTE:
        print("先手の番です。")
    elif turn == BOARD_GOTE:
        print("後手の番です。")
    else:
        print("無効なターンです。")


def board_scan(
    board, row0, col0, row_inc, col_inc, turn
):  # 練習4_方向ごとの反転可能な石の数を数える
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


def board_movable(board, row, col, turn):  # 練習5_指定位置に石を置けるか判定
    if board[row][col] != BOARD_EMPTY:
        return False
    for row_inc, col_inc in BOARD_DIRECTIONS:
        if board_scan(board, row, col, row_inc, col_inc, turn) > 0:
            return True
    return False


def board_movable_any(board, turn):  # 練習6＿合法手があるか判定
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board_movable(board, row, col, turn):
                return True
    return False


def board_move(board, row, col, turn):  # 練習7_石を置き、反転させる
    if not board_movable(board, row, col, turn):
        return False
    board[row][col] = turn
    for row_inc, col_inc in BOARD_DIRECTIONS:
        count = board_scan(board, row, col, row_inc, col_inc, turn)
        for i in range(1, count + 1):
            board[row + i * row_inc][col + i * col_inc] = turn
    return True


def board_number_check(board, turn):  # 練習8_石の数を数える
    count = 0
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == turn:
                count += 1
    return count


def board_eval(board):  # 練習9_評価関数
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


def board_state(board, turn):  # 練習10_盤面状態
    if board_movable_any(board, turn):
        return None  # ゲーム継続中
    elif board_movable_any(board, change_turn(turn)):
        return "pass"  # パス
    else:
        return float(board_eval(board))  # 終局


def game_result(board, state):  # 練習11_ゲーム結果
    if state > 0:
        result = "Game Won by Sente"
    elif state < 0:
        result = "Game Won by Gote"
    else:
        result = "Draw"

    return f"{result}\nScore is {board_number_check(board, BOARD_SENTE)} - {board_number_check(board, BOARD_GOTE)}"


def play_by_human(board, turn, count):  # 練習12＿人間が入力する
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


def othello(sente_gote, yomi_depth):  # 練習13_オセロゲーム関数を定義
    board = initial_board()
    turn = BOARD_SENTE  # 先手番から開始
    count = 1

    while True:
        print_board(board)
        print_current_turn(turn)
        state = board_state(board, turn)

        if state is None:
            # BOARD_EMPTY が指定されている、またはリストが空の場合はコンピュータ
            if sente_gote == [BOARD_EMPTY] or sente_gote == []:
                play_by_machine(board, turn, count, yomi_depth)
            # そうではなく、現在のターンが sente_gote に含まれているならコンピュータ
            elif turn in sente_gote:
                play_by_machine(board, turn, count, yomi_depth)
            # それ以外は「人間」
            else:
                play_by_human(board, turn, count)

            count += 1

        elif state == "pass":
            print(f"{BOARD_SYMBOL[turn]} has no valid moves. Passing turn.")
            turn = change_turn(turn)
            continue

        else:
            print(game_result(board, state))
            break

        turn = change_turn(turn)


# othello(None)  # ゲームを開始


class Node:
    def __init__(self, board, turn, row, col, value):
        self.board = board  # 盤面の状態
        self.turn = turn  # 現在の手番
        self.row = row
        self.col = col
        self.value = value  # 評価


def node_state(node, turn, count):  # 節点の状態
    return board_state(node.board, turn)


# def eval_node(node, turn, count):  # 節点の評価
#    return board_eval(node.board)


def expand_node(parent, turn):  # 練習15_節点の展開
    children = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board_movable(parent.board, row, col, turn):  # 引数を正しく4つ渡す
                new_board = [r[:] for r in parent.board]  # 盤面をコピー
                board_move(new_board, row, col, turn)  # 石を置く

                child_node = Node(new_board, turn, row, col, 0.0)
                children.append(child_node)

    return children


def minimax(node, turn, count, depth):  # 練習16_ミニマックス法

    state = node_state(node, turn, count)
    node_check()

    # state が float なら終局
    if isinstance(state, float):
        node.value = state
        return node

    # depth == 0 なら評価関数を呼び出す
    if depth == 0:
        node.value = eval_node(node, turn, count)
        return node

    # state == "pass" なら、手番を交代して同じ節点から探索を続ける
    if state == "pass":
        next_turn = change_turn(turn)
        return minimax(node, next_turn, count + 1, depth)

    #  それ以外なら、子節点を作って minimax_children() に渡す
    else:
        children = expand_node(node, turn)
        return minimax_children(children, turn, count, depth)


def minimax_children(
    children, turn, count, depth
):  # 練習17_探索子節点の中から最善手を選ぶ
    new_turn = change_turn(turn)
    new_depth = depth - 1
    new_count = count + 1
    val = None
    result_node = None
    for child in children:
        v = minimax(child, new_turn, new_count, new_depth).value
        if (
            val is None
            or (turn == BOARD_SENTE and v > val)
            or (turn == BOARD_GOTE and v < val)
        ):
            val = v
            result_node = Node(child.board, child.turn, child.row, child.col, v)
    return result_node

    # def play_by_machine(board, turn, count, depth):  # 練習18_コンピュータの着手
    # root = Node(board, turn, 0, 0, 0.0)
    # best_node = minimax(root, turn, count, depth)
    # row, col = best_node.row, best_node.col
    # board_move(board, row, col, turn)
    # print(f"({count}) My move is {row + 1} {col + 1}.")


# othello([BOARD_GOTE], 3)  # 人間先手 vs コンピュータ後手
# othello([BOARD_SENTE], 3)  # コンピュータ先手 vs 人間後手
# othello([BOARD_EMPTY], 2)  # コンピュータ vs コンピュータ


def alpha_beta(node, turn, count, depth, alpha, beta):  # 練習20_アルファベータ法
    state = node_state(node, turn, count)
    node_check()

    # state が float なら終局
    if isinstance(state, float):
        node.value = state
        return node

    # depth == 0 なら評価関数を呼び出す
    if depth == 0:
        node.value = eval_node(node, turn, count)
        return node

    # state == "pass" なら、手番を交代して同じ節点から探索を続ける
    if state == "pass":
        next_turn = change_turn(turn)
        return alpha_beta(node, next_turn, count + 1, depth, alpha, beta)

    # それ以外なら、子節点を作って alpha_beta_children() に渡す
    else:
        children = expand_node(node, turn)
        return alpha_beta_children(children, turn, count, depth, alpha, beta)


def alpha_beta_children(
    children, turn, count, depth, alpha, beta
):  # 練習21_探索子節点の中から最善手を選ぶ
    new_turn = change_turn(turn)
    new_depth = depth - 1
    new_count = count + 1
    val = None
    result_node = None
    for child in children:
        v = alpha_beta(child, new_turn, new_count, new_depth, alpha, beta).value
        if turn == BOARD_SENTE:
            if val is None or v > val:
                val = v
                result_node = Node(child.board, child.turn, child.row, child.col, v)
            if v > alpha:
                alpha = v
        elif turn == BOARD_GOTE:
            if val is None or v < val:
                val = v
                result_node = Node(child.board, child.turn, child.row, child.col, v)
            if v < beta:
                beta = v
        if alpha >= beta:
            break
    return result_node


def play_by_machine(
    board, turn, count, depth
):  # 練習22_コンピュータの着手（アルファベータ法）
    node_check_begin()

    node = Node(board, turn, 0, 0, 0.0)
    start = time.perf_counter()
    # best_node = minimax(node, turn, count, depth)
    best_node = alpha_beta(node, turn, count, depth, -math.inf, math.inf)
    row, col = best_node.row, best_node.col
    board_move(board, row, col, turn)
    print(f"({count}) My move is {row + 1} {col + 1}.")
    elapsed = time.perf_counter() - start
    print(f"{elapsed:.3f} sec")

    node_check_end()


def node_check_begin():
    global NODE_CHECK_COUNT
    NODE_CHECK_COUNT = 0


def node_check():
    global NODE_CHECK_COUNT
    NODE_CHECK_COUNT += 1


def node_check_end():
    print(f"{NODE_CHECK_COUNT} nodes checked.")


# othello([BOARD_GOTE], 4)  # 人間先手 vs コンピュータ後手
# othello([BOARD_SENTE], 3)  # コンピュータ先手 vs 人間後手
# othello([BOARD_EMPTY], 2)  # コンピュータ vs コンピュータ
# othello([None], 2)  # 人間vs人園


def board_eval2(board, omomi):  # 練習26_位置点による評価を実装する
    count = 0.0

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            count += board[row][col] * BOARD_POINT[row][col]

    return count * omomi


def board_eval3(board, turn, omomi):  # 練習27：合法手の位置を評価する
    count = 0.0
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board_movable(board, row, col, turn):
                count += turn * (BOARD_POINT[row][col] + omomi)
    return count


def kakutei_scan(
    board, row0, col0, row_inc, col_inc, turn
):  # 練習28：1方向の確定石を数える
    row = row0
    col = col0
    length = 0
    while 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and board[row][col] == turn:
        length += turn  # 先手なら +1、後手なら -1
        row += row_inc
        col += col_inc
        if turn == BOARD_SENTE and length > 0:
            return length - 1  # 先手の確定石数を返す
        elif turn == BOARD_GOTE and length < 0:
            return length + 1  # 後手の確定石数を返す
    return length


def board_eval4(board, omomi):  # 練習29：角からの確定石を評価する
    count = 0.0
    if board[0][0] != BOARD_EMPTY:
        turn = board[0][0]
        count += kakutei_scan(board, 0, 0, 1, 0, turn)  # 下方向
        count += kakutei_scan(board, 0, 0, 0, 1, turn)  # 右方向
    if board[7][7] != BOARD_EMPTY:
        turn = board[7][7]
        count += kakutei_scan(board, 7, 7, -1, 0, turn)  # 上方向
        count += kakutei_scan(board, 7, 7, 0, -1, turn)  # 左方向
    if board[0][7] != BOARD_EMPTY:
        turn = board[0][7]
        count += kakutei_scan(board, 0, 7, 1, 0, turn)  # 下方向
        count += kakutei_scan(board, 0, 7, 0, -1, turn)  # 左方向
    if board[7][0] != BOARD_EMPTY:
        turn = board[7][0]
        count += kakutei_scan(board, 7, 0, -1, 0, turn)  # 上方向
        count += kakutei_scan(board, 7, 0, 0, 1, turn)  # 右方向
    return count * omomi


def board_eval5(board, turn, omomi):  # 練習30：X打ちを減点する
    count = 0.0
    if board[1][1] == turn and board[0][0] == BOARD_EMPTY:
        count += turn * -1
    if board[1][6] == turn and board[0][7] == BOARD_EMPTY:
        count += turn * -1
    if board[6][1] == turn and board[7][0] == BOARD_EMPTY:
        count += turn * -1
    if board[6][6] == turn and board[7][7] == BOARD_EMPTY:
        count += turn * -1
    return count * omomi

    # def eval_node(node, turn, count):  # 練習31：eval_node() を改良する
    # board = node.board
    if count < 25:
        return board_eval2(board, 3) + board_eval(board)  # 序盤
    elif count < 40:
        return board_eval2(board, 3) + board_eval(board)  # 中盤
    elif count < 60:
        return board_eval2(board, 3) + board_eval(board)  # 終盤前
    else:
        return board_eval(board)  # 終盤

    # def eval_node(node, turn, count):  # 練習31：eval_node() 完成版
    # board = node.board
    if count < 25:  # 序盤
        return (
            board_eval2(board, 3)
            + board_eval3(board, turn, 20)
            + board_eval4(board, 100)
            + board_eval5(board, turn, 500)
        )
    elif count < 40:  # 中盤
        return (
            board_eval2(board, 3)
            + board_eval3(board, turn, 40)
            + board_eval4(board, 100)
        )
    elif count < 60:  # 終盤前
        return (
            board_eval2(board, 3)
            + board_eval3(board, turn, 20)
            + board_eval4(board, 100)
        )
    else:  # 終盤
        return board_eval(board)


def make_eval_node(weights):
    """重みベクトルから eval_node 関数を作成して返す。"""
    w2, w3, w4, w5 = weights

    def eval_node(node, turn, count):
        board = node.board
        if count < 25:
            return (
                board_eval2(board, w2)
                + board_eval3(board, turn, w3)
                + board_eval4(board, w4)
                + board_eval5(board, turn, w5)
            )
        elif count < 40:
            return (
                board_eval2(board, w2)
                + board_eval3(board, turn, w3 * 2)
                + board_eval4(board, w4)
            )
        elif count < 60:
            return (
                board_eval2(board, w2)
                + board_eval3(board, turn, w3)
                + board_eval4(board, w4)
            )
        else:
            return board_eval(board)

    return eval_node


# モジュール全体で使う「現在の評価関数」を保持する
_current_eval_node = None


def set_eval_node(fn):
    global _current_eval_node
    _current_eval_node = fn


def eval_node(node, turn, count):
    return _current_eval_node(node, turn, count)


def legal_moves(board, turn):
    return [
        (r, c)
        for r in range(BOARD_SIZE)
        for c in range(BOARD_SIZE)
        if board_movable(board, r, c, turn)
    ]


# 練習33：適合度関数を実装する
def play_one_game(eval_sente, eval_gote, depth, opening_random=4, rng=None):
    """eval_sente を先手、eval_gote を後手として 1 局対戦し勝者を返す。"""
    rng = rng or random
    board = initial_board()
    turn = BOARD_SENTE
    count = 1
    move_number = 0
    while True:
        state = board_state(board, turn)
        if isinstance(state, float):
            break
        if state == "pass":
            turn = change_turn(turn)
            count += 1
            continue
        if move_number < opening_random:
            row, col = rng.choice(legal_moves(board, turn))
        else:
            set_eval_node(eval_sente if turn == BOARD_SENTE else eval_gote)
            node = Node(board, turn, 0, 0, 0.0)
            best = alpha_beta(node, turn, count, depth, -math.inf, math.inf)
            row, col = best.row, best.col
        board_move(board, row, col, turn)
        turn = change_turn(turn)
        count += 1
        move_number += 1
    sente = board_number_check(board, BOARD_SENTE)
    gote = board_number_check(board, BOARD_GOTE)
    return BOARD_SENTE if sente > gote else BOARD_GOTE if gote > sente else 0


def fitness(weights, baseline, n_games, depth):
    eval_w = make_eval_node(weights)
    eval_b = make_eval_node(baseline)
    wins = 0
    # 公平のため、先手・後手を交代しながら半分ずつ対戦する
    for i in range(n_games):
        if i % 2 == 0:
            winner = play_one_game(eval_w, eval_b, depth)
            if winner == BOARD_SENTE:
                wins += 1
        else:
            winner = play_one_game(eval_b, eval_w, depth)
            if winner == BOARD_GOTE:
                wins += 1
    return wins


def hill_climbing(
    initial_weights, max_iter, sigma, baseline, n_games, depth
):  # 練習34：山登り法を実装する
    current = list(initial_weights)
    current_fitness = fitness(current, baseline, n_games, depth)
    history = [(0, current[:], current_fitness)]

    for t in range(1, max_iter + 1):
        neighbor = [w + random.gauss(0, sigma) for w in current]
        neighbor = [max(0.0, w) for w in neighbor]  # 重みは非負に制限
        neighbor_fitness = fitness(neighbor, baseline, n_games, depth)
        if neighbor_fitness > current_fitness:
            current = neighbor
            current_fitness = neighbor_fitness
        history.append((t, current[:], current_fitness))

    return current, history


# まず w4 (確定石) だけを動かす
def fitness_w4(w4, baseline, n_games, depth):  # 練習35：1 次元から動作確認
    weights = list(baseline)
    weights[2] = w4  # baseline の他の重みは固定、w4 だけ可変
    return fitness(weights, baseline, n_games, depth)


# baseline_weights = [3.0, 20.0, 100.0, 500.0]  # 元のコードに登場する初期基準
# w4_values = [0, 50, 100, 200, 500, 1000]
# fitness_scores = []

# print("--- 練習35: w4の1次元動作確認 ---")
# for w4 in w4_values:
# 20試合対戦（先手10回・後手10回）させて勝数をカウント
# score = fitness_w4(w4, baseline=baseline_weights, n_games=20, depth=2)
# fitness_scores.append(score)
# print(f"w4 = {w4:4d} | 適合度 (勝数): {score}/20")

# グラフのプロット
# plt.figure(figsize=(6, 4))
# plt.plot(w4_values, fitness_scores, marker="o", color="b", linestyle="-")
# plt.title("Practice 35: Fitness vs w4 Value")
# plt.xlabel("w4 (Stable Disks Weight)")
# plt.ylabel("Fitness (Wins out of 20)")
# plt.grid(True)
# plt.savefig("w4_練習35.png")
# plt.show()

# print("\n--- 練習36: 4次元山登り法を開始 ---")

# 初期重みと、山登り法の実行
# initial_w = [3.0, 20.0, 100.0, 500.0]
# best_w, history = hill_climbing(
# initial_weights=initial_w,
# max_iter=30,  # 反復回数（実験のため少なめに設定、本来は100以上推奨）
# sigma=10.0,  # ステップサイズ（ノイズの大きさ）
# baseline=initial_w,
# n_games=8,  # 1世代あたりの対戦数
# depth=2,
# )

# print(f"\n探索完了 最良の重み: {best_w}")

# 適合度の推移をプロット
# iterations = [item[0] for item in history]
# fitness_history = [item[2] for item in history]

# plt.figure(figsize=(6, 4))
# plt.plot(iterations, fitness_history, marker="s", color="r")
# plt.title("Practice 36: Hill Climbing Progress")
# plt.xlabel("Iteration (t)")
# plt.ylabel("Current Weights Fitness")
# plt.grid(True)
# plt.savefig("w4_練習36.png")
# # plt.show()


def simulated_annealing(
    initial_weights, max_iter, sigma, T0, T_end, baseline, n_games, depth
):  # 練習37：焼きなまし法を実装する
    current = list(initial_weights)
    current_fitness = fitness(current, baseline, n_games, depth)
    best, best_fitness = current[:], current_fitness
    history = [(0, current[:], current_fitness)]

    for t in range(1, max_iter + 1):
        T = T0 * (T_end / T0) ** (t / max_iter)  # 指数冷却
        neighbor = [max(0.0, w + random.gauss(0, sigma)) for w in current]
        nf = fitness(neighbor, baseline, n_games, depth)
        if nf > current_fitness:
            current, current_fitness = neighbor, nf
        else:
            if random.random() < math.exp((nf - current_fitness) / max(T, 1e-9)):
                current, current_fitness = neighbor, nf
        if current_fitness > best_fitness:
            best, best_fitness = current[:], current_fitness
        history.append((t, current[:], current_fitness))

    return best, history

    # 実験の共通設定
    # initial_w = [3.0, 20.0, 100.0, 500.0]
    # max_iter = 40
    # sigma = 15.0
    # n_games = 10
    # depth = 2

    # パターン1: 標準的な設定
    # print("\n--- [1] 標準設定での実験 ---")
    # best_std, hist_std = simulated_annealing(
    (initial_w,)
    (max_iter,)
    (sigma,)
    T0 = (10.0,)
    T_end = (0.1,)
    baseline = (initial_w,)
    n_games = (n_games,)
    depth = (depth,)
    # )

    # パターン2: T0が大きすぎる
    # print("\n--- [2] T0が大きすぎる実験 (ランダムウォーク) ---")
    # best_high, hist_high = simulated_annealing(
    (initial_w,)
    (max_iter,)
    (sigma,)
    T0 = (1000.0,)
    T_end = (100.0,)
    baseline = (initial_w,)
    n_games = (n_games,)
    depth = (depth,)
    # )

    # パターン3: T0が小さすぎる
    # print("\n--- [3] T0が小さすぎる実験 (山登り法化) ---")
    # best_low, hist_low = simulated_annealing(
    (initial_w,)
    (max_iter,)
    (sigma,)
    T0 = (0.001,)
    T_end = (0.0001,)
    baseline = (initial_w,)
    n_games = (n_games,)
    depth = (depth,)
    # )

    # --- グラフの描画 ---
    # plt.figure(figsize=(10, 6))

    # plt.plot(
    ([h[0] for h in hist_std],)
    ([h[2] for h in hist_std],)
    label = ("Standard (T0=10.0, Tend=0.1)",)
    color = ("green",)
    linewidth = (2,)
    # )
    # plt.plot(
    ([h[0] for h in hist_high],)
    ([h[2] for h in hist_high],)
    label = ("Too High T0 (1000.0) -> Random Walk",)
    color = ("red",)
    linestyle = ("--",)
    # )
    # plt.plot(
    ([h[0] for h in hist_low],)
    ([h[2] for h in hist_low],)
    label = ("Too Low T0 (0.001) -> Hill Climbing",)
    color = ("blue",)
    linestyle = (":",)


# )

# plt.title("Practice 38: Effect of Temperature Schedules")
# plt.xlabel("Iteration (t)")
# plt.ylabel("Current Fitness (Wins)")
# plt.grid(True)
# plt.legend()
# plt.savefig("温度スケジュールの影響_練習38.png", dpi=300, bbox_inches="tight")
# plt.show()


def tournament_select(population, fitnesses, k=3):  # 練習39：トーナメント選択
    """k 個をランダムに選び、その中で最良の個体を返す"""
    candidates = random.sample(range(len(population)), k)
    best = max(candidates, key=lambda i: fitnesses[i])
    return population[best]


def crossover(a, b):  # 練習40：交叉と突然変異
    """一様交叉：各次元について確率 0.5 で親を入れ替える"""
    c = [a[i] if random.random() < 0.5 else b[i] for i in range(len(a))]
    d = [b[i] if random.random() < 0.5 else a[i] for i in range(len(a))]
    return c, d


def mutate(individual, sigma, pm):
    """各次元に確率 pm でガウス雑音を加える"""
    return [
        max(0.0, w + random.gauss(0, sigma)) if random.random() < pm else w
        for w in individual
    ]


def genetic_algorithm(
    pop_size, generations, baseline, n_games, depth, sigma=20.0, pc=0.8, pm=0.2
):  # 練習41：GA 本体
    # 初期集団：baseline まわりの乱数で初期化
    population = [
        [max(0.0, w + random.gauss(0, sigma * 2)) for w in baseline]
        for _ in range(pop_size)
    ]
    history = []

    for g in range(generations):
        fitnesses = [fitness(ind, baseline, n_games, depth) for ind in population]
        best_idx = max(range(pop_size), key=lambda i: fitnesses[i])
        history.append((g, population[best_idx][:], fitnesses[best_idx]))

        new_pop = [population[best_idx][:]]  # エリート保存
        while len(new_pop) < pop_size:
            a = tournament_select(population, fitnesses)
            b = tournament_select(population, fitnesses)
            if random.random() < pc:
                c, d = crossover(a, b)
            else:
                c, d = a[:], b[:]
            c = mutate(c, sigma, pm)
            d = mutate(d, sigma, pm)
            new_pop.append(c)
            if len(new_pop) < pop_size:
                new_pop.append(d)
        population = new_pop

    fitnesses = [fitness(ind, baseline, n_games, depth) for ind in population]
    best_idx = max(range(pop_size), key=lambda i: fitnesses[i])
    return population[best_idx], history


# 共通のベースライン設定
initial_w = [3.0, 20.0, 100.0, 500.0]
depth = 2
n_games_common = 10  # 1回の適合度測定に使う試合数

print("--- 練習42: 3大アルゴリズムの公平比較実験を開始（総予算200試合） ---")

# 1. 山登り法 (反復20 × 10試合 = 200)
print("\n[実行中] 山登り法...")
_, hc_history = hill_climbing(
    initial_weights=initial_w,
    max_iter=20,
    sigma=15.0,
    baseline=initial_w,
    n_games=n_games_common,
    depth=depth,
)

# 2. 焼きなまし法 (反復20 × 10試合 = 200)
print("\n[実行中] 焼きなまし法...")
_, sa_history = simulated_annealing(
    initial_weights=initial_w,
    max_iter=20,
    sigma=15.0,
    T0=10.0,
    T_end=0.1,
    baseline=initial_w,
    n_games=n_games_common,
    depth=depth,
)

# 3. 遺伝学的アルゴリズム (個体5 × 世代4 × 10試合 = 200)
print("\n[実行中] 遺伝学的アルゴリズム...")
_, ga_history = genetic_algorithm(
    pop_size=5,
    generations=4,
    baseline=initial_w,
    n_games=n_games_common,
    depth=depth,
    sigma=15.0,
)

# --- 各データの「消費した総ゲーム数（横軸）」を計算してプロット ---
# 横軸を「世代/反復数」ではなく「それまでに消費した総ゲーム数」に揃えることで、真の効率が見えます。
hc_games = [h[0] * n_games_common for h in hc_history]
hc_fits = [h[2] for h in hc_history]

sa_games = [s[0] * n_games_common for s in sa_history]
sa_fits = [s[2] for s in sa_history]

# GAは各世代の終わりに pop_size * n_games ずつ消費していく
ga_games = [(g[0] + 1) * 5 * n_games_common for g in ga_history]
ga_fits = [g[2] for g in ga_history]
# スタート地点（0試合時点）として初期の最高値を先頭に補完
ga_games.insert(0, 0)
ga_fits.insert(0, hc_fits[0])

# --- グラフ描画と自動保存 ---
plt.figure(figsize=(10, 6))

plt.plot(hc_games, hc_fits, marker="o", label="Hill Climbing", color="blue")
plt.plot(sa_games, sa_fits, marker="s", label="Simulated Annealing", color="green")
plt.plot(
    ga_games, ga_fits, marker="^", label="Genetic Algorithm", color="red", linewidth=2
)

plt.title("Practice 42: Optimization Performance Comparison (Budget = 200 Games)")
plt.xlabel("Total Evaluated Games (Computational Cost)")
plt.ylabel("Best Fitness (Wins)")
plt.xlim(0, 200)
plt.grid(True)
plt.legend()

# 高画質（dpi=300）で枠外はみ出しを防いで保存
plt.savefig("練習42.png", dpi=300, bbox_inches="tight")
plt.show()

# --- 最終最良適合度と最良重みの表示システム ---
print("\n" + "=" * 80)
print(
    f"{'アルゴリズム':<25} | {'最終最良適合度':<12} | {'最良重みベクトル [w2, w3, w4, w5]':<30}"
)
print("=" * 80)

# 1. 山登り法（historyの最後の要素から取得）
hc_final_step = hc_history[-1]
hc_best_weight = hc_final_step[1]
hc_best_fit = hc_final_step[2]
hc_weight_str = f"[{', '.join([f'{w:.2f}' for w in hc_best_weight])}]"
print(f"{'Hill Climbing':<25} | {hc_best_fit:<12d} | {hc_weight_str:<30}")

# 2. 焼きなまし法（変数の直参照を避け、sa_historyの全履歴から最高値を自動抽出）
# 履歴の中で一番高い勝数（適合度）を持つインデックスを見つける
sa_best_idx = max(range(len(sa_history)), key=lambda i: sa_history[i][2])
sa_best_step = sa_history[sa_best_idx]
sa_best_weight = sa_best_step[1]
sa_best_fit = sa_best_step[2]
sa_weight_str = f"[{', '.join([f'{w:.2f}' for w in sa_best_weight])}]"
print(f"{'Simulated Annealing':<25} | {sa_best_fit:<12d} | {sa_weight_str:<30}")

# 3. 遺伝学的アルゴリズム（ga_historyの最後の要素から取得）
ga_final_step = ga_history[-1]
ga_best_weight = ga_final_step[1]
ga_best_fit = ga_final_step[2]
ga_weight_str = f"[{', '.join([f'{w:.2f}' for w in ga_best_weight])}]"
print(f"{'Genetic Algorithm':<25} | {ga_best_fit:<12d} | {ga_weight_str:<30}")

print("=" * 80)


print("\n" + "=" * 40)
print(" 練習43：考察データの収集シミュレーション")
print("=" * 40)

# 1. 基準AI（ベースライン）とは全く異なる、位置点・確定石を極端に重視した「未知の強敵」を用意
test_opponent_weight = [10.0, 5.0, 300.0, 1000.0]
eval_test_opponent = make_eval_node(test_opponent_weight)

# --- 💡 履歴リスト(history)から最良の重みを安全に自動抽出 ---
# ① 山登り法
hc_best_idx = max(range(len(hc_history)), key=lambda i: hc_history[i][2])
w_hc = hc_history[hc_best_idx][1]

# ② 焼きなまし法
sa_best_idx = max(range(len(sa_history)), key=lambda i: sa_history[i][2])
w_sa = sa_history[sa_best_idx][1]

# ③ 遺伝学的アルゴリズム
ga_best_idx = max(range(len(ga_history)), key=lambda i: ga_history[i][2])
w_ga = ga_history[ga_best_idx][1]

algorithms = {
    "Hill Climbing": w_hc,
    "Simulated Annealing": w_sa,
    "Genetic Algorithm": w_ga,
}

print("\n【実験①】未知のテストプレイヤーとの対戦（過学習の検証）")
print(
    "※学習相手（ベースライン）以外にも汎用的に強いかを50試合（先後交代）で測定します。"
)
print("-" * 80)
print(f"{'アルゴリズム':<20} | {'対テストプレイヤー勝数':<22} | {'勝率':<8}")
print("-" * 80)

test_games = 50
for name, weight in algorithms.items():
    eval_candidate = make_eval_node(weight)

    # 汎化性能テスト
    wins = 0
    for i in range(test_games):
        if i % 2 == 0:
            winner = play_one_game(eval_candidate, eval_test_opponent, depth=2)
            if winner == BOARD_SENTE:
                wins += 1
        else:
            winner = play_one_game(eval_test_opponent, eval_candidate, depth=2)
            if winner == BOARD_GOTE:
                wins += 1

    win_rate = (wins / test_games) * 100
    print(f"{name:<20} | {wins:<5d} / {test_games:<14d} | {win_rate:.1f}%")

print("-" * 80)


print("\n【実験②】評価ノイズ（再現性）の検証")
print("※同じ重みでも、ランダム要素によって勝率がどれくらいブレるかを3回再測定します。")
print("-" * 80)
print(
    f"{'アルゴリズム':<20} | {'測定1 (10局)':<12} | {'測定2 (10局)':<12} | {'測定3 (10局)':<12}"
)
print("-" * 80)

# 最初の共通ベースライン初期値 [3.0, 20.0, 100.0, 500.0] を指定
initial_w = [3.0, 20.0, 100.0, 500.0]

for name, weight in algorithms.items():
    scores = []
    for _ in range(3):
        score = fitness(weight, baseline=initial_w, n_games=10, depth=2)
        scores.append(score)
    print(f"{name:<20} | {scores[0]:<12d} | {scores[1]:<12d} | {scores[2]:<12d}")

print("-" * 80)
