from reversi_2420204 import (
    BOARD_SENTE,
    BOARD_GOTE,
    BOARD_EMPTY,
    BOARD_SIZE,
    initial_board,
    change_turn,
    board_movable,
    board_movable_any,
    board_move,
    board_number_check,
    board_scan,
    board_eval,
    board_state,
    game_result,
    play_by_human,
    othello,
)


def test_initial_board():  # 練習1
    board = initial_board()
    assert board[3][3] == BOARD_GOTE
    assert board[3][4] == BOARD_SENTE
    assert board[4][3] == BOARD_SENTE
    assert board[4][4] == BOARD_GOTE
    assert board[0][0] == BOARD_EMPTY


def test_change_turn():  # 練習2
    assert change_turn(BOARD_SENTE) == BOARD_GOTE
    assert change_turn(BOARD_GOTE) == BOARD_SENTE


def test_board_scan():  # 練習4
    board = initial_board()
    assert board_scan(board, 2, 3, 1, 0, BOARD_SENTE) == 1
    assert board_scan(board, 2, 2, 1, 1, BOARD_SENTE) == 0
    assert board_scan(board, 0, 0, 1, 1, BOARD_SENTE) == 0


def test_board_movable():  # 練習5
    board = initial_board()
    assert board_movable(board, 2, 3, BOARD_SENTE)
    assert not board_movable(board, 2, 3, BOARD_GOTE)
    assert not board_movable(board, 3, 3, BOARD_SENTE)


def test_board_movable_any():  # 練習6
    board = initial_board()
    assert board_movable_any(board, BOARD_SENTE)
    assert board_movable_any(board, BOARD_GOTE)


def test_board_move():  # 練習7
    board = initial_board()
    board_move(board, 2, 3, BOARD_SENTE)
    assert board[2][3] == BOARD_SENTE
    assert board[3][3] == BOARD_SENTE


def test_board_number_check():  # 練習8
    board = initial_board()
    assert board_number_check(board, BOARD_SENTE) == 2
    assert board_number_check(board, BOARD_GOTE) == 2


def test_board_eval():  # 練習9
    board = initial_board()
    assert board_eval(board) == 0.0


def test_board_state():  # 練習10
    board = initial_board()
    assert board_state(board, BOARD_SENTE) is None
    assert board_state(board, BOARD_GOTE) is None


def test_game_result():  # 練習11
    board = initial_board()
    state = board_eval(board)
    result = game_result(board, state)
    assert "Score is" in result


# def test_play_by_human():  # 練習12
# board = initial_board()
# turn = BOARD_SENTE
# count = 0
# play_by_human(board, turn, count)


def test_othello():  # 練習13
    sente_gote = (BOARD_SENTE, BOARD_GOTE)
    # othello(sente_gote)


def expand_node(parent, turn):
    root = Node(initial_board(), BOARD_SENTE, 0, 0, 0.0)
    children = expand_node(root, BOARD_SENTE)
    assert len(children) == 4
    assert all(isinstance(child, Node) for child in children)
