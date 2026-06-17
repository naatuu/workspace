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


# def test_change_turn():  # 練習2
#    assert change_turn(BOARD_SENTE) == BOARD_GOTE
#    assert change_turn(BOARD_GOTE) == BOARD_SENTE


# def test_board_scan(board, row0, col0, row_inc, col_inc, turn):  # 練習4
#   board = initial_board()
#    assert test_board_scan(board, 2, 3, 1, 0, BOARD_SENTE) == 1
#    assert test_board_scan(board, 2, 2, 1, 1, BOARD_SENTE) == 0
#    assert test_board_scan(board, 0, 0, 1, 1, BOARD_SENTE) == 0


# def test_board_movable(board, row, col, turn):  # 練習5
#    pass


# def test_board_movable_any(board, turn):  # 練習6
#    pass


# def test_board_move(board, row, col, turn):  # 練習7
#    pass


# def test_board_number_check(board, turn):  # 練習8
#    pass


# def test_board_eval(board):  # 練習9
#    pass


# def test_board_state(board, turn):  # 練習10
#    pass


# def test_game_result(board, state):  # 練習11
#    pass


# def test_play_by_human(board, turn, count):  # 練習12
#    pass


# def test_othello(sente_gote, yomi_depth=None):  # 練習13
#    pass
