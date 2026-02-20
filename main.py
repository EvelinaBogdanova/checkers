import pygame, sys
from pygame.locals import *

pygame.font.init()

WHITE   = (255, 255, 255)
BLUE    = (  0,   0, 255)
RED     = (255,   0,   0)
BLACK   = (  0,   0,   0)
GOLD    = (255, 215,   0)
HIGH    = (160, 190, 255)

NORTHWEST = "northwest"
NORTHEAST = "northeast"
SOUTHWEST = "southwest"
SOUTHEAST = "southeast"

class Game:
    def __init__(self):
        self.graphics = Graphics()
        self.board = Board()

        self.turn = BLUE
        self.selected_piece = None
        self.hop = False
        self.selected_legal_moves = []

    def setup(self):
        self.graphics.setup_window()

    def even_loop(self):
        self.mouse_pos = self.graphics.board_coords(pygame.mouse.get_pos())
        if self.selected_piece != None:
            self.selected_legal_moves = self.board.legal_moves(self.selected_piace, self.hop)

        for event in pygame.event.get():

            if event.type == QUIT:
                self.teminate_game()

            if event.type == MOUSEBUTTONDOWN:
                if self.hop == False:
                    if self.board.location(self.mouse_pos).occupant != None and self.board.location(self.mouse_pos).occupant.color == self.turn:
                        self.selected_piece = self.mouse_pos

                    elif self.selected_piece != None and self.mouse_pos in self.board.legal_moves(self.selected_piece):

                        self.board.move_piace(self.selected_piece, self.mouse_pos)

                        if self.mouse_pos not in self.board.adjacent(self.selected_piece):
                            self.board.remove_piece(((self.selected_piece[0] + self.mouse_pos[0]) >> 1, (self.selected_piece[1] + self.mouse_pos[1]) >> 1))

                            self.hop = True
                            self.selected_piece = self.mouse_pos

                        else:
                            self.end_turn()

                if self.hop == True:
                    if self.selected_piece != None and self.mouse_pos in self.board.legal_moves(self.selected_piece, self.hop):
                        self.board.move_piece(self.selected_piece, self.mouse_pos)
                        self.board.remove_piece(((self.selected_piece[0] + self.mouse_pos[0]) >> 1, (self.selected_piece[1] + self.mouse_pos[1]) >> 1))

                    if self.board.legal_moves(self.mouse_pos, self.hop) == []:
                        self.end_turn()

                    else:
                        self.salected_piece = self.mouse_pos