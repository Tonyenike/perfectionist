import sys
import numpy as np
from copy import deepcopy
from solver import solve
from fetch_daily_board import fetch_daily_board, fetch_weekly_board, fetch_board

RESULTS_FILE = "results.log"
RESULTS_FILE_HTML = "output.html"
FEVER = 10

class PerfectionistBoard:
    def __init__(self, board):

        self.height = len(board)
        self.width = len(board[0])

        self.size = self.width * self.height

        self.board = board.flatten()
        self.count = np.count_nonzero(self.board)

        self.lost = 0

        self.global_best = sum(self.board)
        self.path = []

    def __hash__(self):
        return hash(str(self.board))

    def __eq__(self, other):
        board_equality = np.array(self.board) == np.array(other.board)
        return self.lost == other.lost and board_equality.all()

    def __repr__(self):
        i = 0
        outstr = "\n" + "-" * (self.width * 3 + 2) + "\n"
        for yy in range(self.height):
            outstr += "|"
            for xx in range(self.width):
                xx, yy
                outstr += str(self.board[i]).rjust(2, " ") + " "
                i += 1
            outstr += "|\n"
        outstr += "-" * (self.width * 3 + 2)
        return outstr

    def export_move_sequence(self, moves):
        orig_stdout = sys.stdout
        sys.stdout = open(RESULTS_FILE, "w")
        self_copy = deepcopy(self)
        for i in range(len(moves)):
            print(self_copy)
            self_copy.do_move(moves[i])
        print(self_copy)
        sys.stdout = orig_stdout

    def export_move_sequence_html(self, moves):
        orig_stdout = sys.stdout
        sys.stdout = open(RESULTS_FILE_HTML, "w")
        self_copy = deepcopy(self)
        style_str = "<style>p{font-family: courier; white-space: pre}span{color:red;}</style>"
        print("<!DOCTYPE html><html><head>" + style_str + "</head><body><p>")
        for i in range(len(moves)):
            print(self_copy.show_move_html(moves[i]))
            self_copy.do_move(moves[i])
        print("</p></body></html>")
        sys.stdout = orig_stdout

    def show_move_html(self, move_to_highlight):
        i = 0
        outstr = "<br>" + "-" * (self.width * 3 + 2) + "<br>"
        for yy in range(self.height):
            outstr += "|"
            for xx in range(self.width):
                xx, yy
                if i in move_to_highlight:
                    outstr += "<span>" + str(self.board[i]).rjust(2, " ") + " " + "</span>"
                else:
                    outstr += str(self.board[i]).rjust(2, " ") + " "
                i += 1
            outstr += "|<br>"
        outstr += "-" * (self.width * 3 + 2)
        return outstr

    def do_move(self, move):
        if self.board[move[0]] == self.board[move[1]] and not move[0] == move[1]:
            lost = 0
            self.count -= 2
        else:
            lost = min(self.board[move[1]], self.board[move[0]])
            self.count -= 1
        self.board[move[1]] = abs(self.board[move[1]] - self.board[move[0]])
        self.board[move[0]] = 0
        self.lost += lost
        self.path.append(move)
        return self

    def try_move(self, move):
        self_copy = deepcopy(self)
        return self_copy.do_move(move)

    def get_good_moves(self, loss_max=15):
        available_moves = []
        for row_step in range(0, self.size, self.width):
            for i in range(row_step, row_step + self.width):
                # If the tile is 1, available moves are to match it to all tiles bigger than 1.
                # We probably don't want to match a 1 to another 1.
                if self.board[i] == 1:
                    for j in range(0, self.size):
                        # We probably don't want to match a 1 to another 1.
                        if self.board[j] > 1:
                            available_moves.append((i, j))
                elif self.board[i]:
                    # Look at subsequent tiles in the same row as i
                    for j in range(i + 1, row_step + self.width):
                        if self.board[j] == self.board[i]:
                            available_moves.append((i, j))
                            break
                        elif self.board[j]:
                            loss_value = min(self.board[j], self.board[i])
                            if loss_value <= loss_max:
                                if j != 1:
                                    available_moves.append((j, i))
                                available_moves.append((i, j))
                            break

                    # Look at subsequent tiles in the same column as i
                    for j in range(i + self.width, self.size, self.width):
                        if self.board[j] == self.board[i]:
                            available_moves.append((i, j))
                            break
                        elif self.board[j]:
                            loss_value = min(self.board[j], self.board[i])
                            if loss_value <= loss_max:
                                if j != 1:
                                    available_moves.append((j, i))
                                available_moves.append((i, j))
                            break
        return available_moves



if __name__ == "__main__":
    game_board = fetch_daily_board(2)
    print(game_board)

    my_perf_board = PerfectionistBoard(game_board)
    solve(my_perf_board)
