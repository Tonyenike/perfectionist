import sys
from get_best_fever_score import FeverBoard
import numpy as np
from operator import itemgetter
from copy import deepcopy

BRANCH_LIMIT = 5000
FEVER = 10



def solve(board):
    best_score = -1
    old_list = [board]

    while len(old_list) != 0:
        available_moves = []
        available_moves_loss = []
        board_idx = []

        current_loss_maximum = 10000000000

        for board_id, current_board in enumerate(old_list):
            if current_board.count <= FEVER:
                current_best_score = current_board.lost + \
                                     FeverBoard(current_board.board[np.nonzero(current_board.board)]). \
                                         get_best_fever_score(threshold_ceiling=best_score - current_board.lost)
                if current_best_score < best_score or best_score == -1:
                    board.export_move_sequence_html(current_board.path)
                    best_score = current_best_score
            else:
                moves_to_consider = current_board.get_good_moves(current_loss_maximum - current_board.lost)
                losses = [current_board.try_move(move).lost for move in moves_to_consider]

                available_moves.extend(moves_to_consider)
                available_moves_loss.extend(losses)
                board_idx.extend([board_id] * len(losses))

                available_moves_loss, board_idx, available_moves = \
                    [list(a) for a in zip(*sorted(zip(available_moves_loss, board_idx, available_moves)))]

                del available_moves_loss[BRANCH_LIMIT:]
                del available_moves[BRANCH_LIMIT:]
                del board_idx[BRANCH_LIMIT:]

                if len(available_moves_loss) == BRANCH_LIMIT:
                    current_loss_maximum = available_moves_loss[BRANCH_LIMIT - 1] - 1

        new_list = set()
        for i in range(len(available_moves)):
            new_list.add(old_list[board_idx[i]].try_move(available_moves[i]))
        old_list = list(new_list)

    return best_score
