#AI player using alpha-beta pruning algorithm implementation

import chess
from gui_components.boards import ChessBoard
import re
from gui_components import pieces
import math
import random

#basic ai player base class
class AIPlayer:
    #initialization
    def __init__(self, board: chess.Board, color: str) -> None:
        self.board = board
        self.color = color

#random AI player used for test cases
class RandomPlayer(AIPlayer):

    #ChessBoard -> string
    #decide random move from legal moves
    def make_move(self, chess_board: ChessBoard):
        legal_moves = list(self.board.legal_moves)
        move = random.choice(legal_moves)
        chess_board._play(move=move)

#ai player with minimax evaluation
class PlayerWithEvaluation(AIPlayer):
    
    #ChessBoard -> int
    #heuristic evalution of the position on board
    def evaluate_board(self, board: chess.Board=None) -> int: #using heuristics in pieces.py
        if board is None: 
            board = self.board
        regex = re.compile("\w")
        string = board.__str__()
        material_sum = 0

        ranks = [ row.split(' ') for row in string.split('\n')]

        for i, rank in enumerate(ranks):
            for j, notation in enumerate(rank):
                if regex.search(notation):
                    piece_color = pieces.Piece.get_piece_color_based_on_notation(notation)
                    piece_positional_value = pieces.Piece.get_piece_value_from_notation_and_position(notation, piece_color, i, j)

                    material_sum += piece_positional_value
        return -material_sum
    
    #int, bool, int, int, ChessBoard -> int
    #Iterates through tree of possible moves, holding max (alpha) and min (beta), returns best evaluation best move
    def minimax(self, depth, isMaximizingPlayer, alpha, beta, board: chess.Board=None):        
        # for child in children:
        if depth == 0 or self.board.is_game_over():
            # print(self.board)
            # print(self.evaluate_board(self.board))
            return self.evaluate_board(self.board)

        if isMaximizingPlayer: #if taking turns as maximizing player
            self.board.turn = False
            max_eval = -math.inf
            # print(self.board.legal_moves)
            for child in self.board.legal_moves:
                self.board.push(child)
                current_eval = self.minimax(depth - 1, False, alpha, beta, self.board)
                # print(self.board)
                # print(current_eval)
                self.board.pop()
                max_eval = max(max_eval, current_eval)
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break
            return max_eval

        else: #if taking turns as minimizing player
            self.board.turn = True
            min_eval = math.inf
            for child in self.board.legal_moves:
                self.board.push(child)
                # print(self.board)
                current_eval = self.minimax(depth - 1, True, alpha, beta, self.board)
                # print(current_eval)
                self.board.pop()
                min_eval = min(min_eval, current_eval)
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break
            return min_eval
    
    #int, ChessBoard -> string
    #iterates through legal moves and uses minimax to find the move with the best eval
    def get_bestmove(self, depth, board: chess.Board = None):
        best_move = None
        max_eval = -math.inf
        for move in self.board.legal_moves:
            self.board.push(move)
            eval = self.minimax(depth -1, True, -math.inf, +math.inf, self.board)
            self.board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
        # print("BEST MOVE IS")
        # print(best_move)
        # print(max_eval)
        return best_move

    #ChessBoard -> None
    #valls best_move to get a move and then plays the move to the chess board
    def make_move(self, chess_board: ChessBoard):
        move = self.get_bestmove(3, chess_board)
        chess_board._play(move=move)


