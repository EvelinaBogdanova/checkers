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

    def update(self):
        self.graphics.update_display(self.board, self.selected_legal_moves, self.selected_piece)

    def terminate_game(self):
        pygame.quit()
        sys.exit()

    def main(self):
        self.setup()

        while True:
            self.event_loop()
            self.update()

    def end_turn(self):
        
        if self.turn == BLUE:
            self.turn = RED

        else:
            self.turn = BLUE

        self.selected_piece = None
        self.selected_legal_moves = []
        self.hop = False

        if self.check_for_endgame():
            if self.turn == BLUE:
                self.graphics.draw_message("RED WINS!")
            else:
                self.graphics.draw_message("BLUE WINS!")

    def check_for_endgame(self):
        for x in range(8):
            for y in range(8):
                location = self.board.location((x, y))
                if location.color == BLACK and location.occupant is not None and location.occupant.color == self.turn:
                    if self.board.legal_moves((x, y)) != []:
                        return False
        return True

    class Graphics:
        def __init__(self):
            self.caption = "Checkers"

            self.fps = 60
            self.clock = pygame.time.Clock()

            self.window_size = 600
            self.screen = pygame.display.set_mode((self.window_size, self.window_size))
            self.background = pygame.image.load('resources/board.png')

            self.square_size = self.window_size >> 3
            self.piece_size = self.square_size >> 1

            self.message = False

    def setup_window(self):
        """
        This initializes the window and sets the caption at the top.
        """
        pygame.init()
        pygame.display.set_caption(self.caption)

    def update_display(self, board, legal_moves, selected_piece):
        """
        This updates the current display.
        """
        self.screen.blit(self.background, (0, 0))

        self.highlight_squares(legal_moves, selected_piece)
        self.draw_board_pieces(board)

        if self.message:
            self.screen.blit(self.text_surface_obj, self.text_rect_obj)

        pygame.display.update()
        self.clock.tick(self.fps)

    def draw_board_squares(self, board):
        for x in range(8):
            for y in range(8):
                pygame.draw.rect(self.screen, board[x][y].color, (x * self.square_size, y * self.square_size, self.square_size, self.square_size), )

    def draw_board_pieces(self, board):
        for x in range(8):
            for y in range(8):
               if board.matrix[x][y].occupant != None:
					pygame.draw.circle(self.screen, board.matrix[x][y].occupant.color, self.pixel_coords((x,y)), self.piece_size) 

					if board.location((x,y)).occupant.king == True:
						pygame.draw.circle(self.screen, GOLD, self.pixel_coords((x,y)), int (self.piece_size / 1.7), self.piece_size >> 2)


    def pixel_coords(self, board_coords):
        return (board_coords[0] * self.square_size + self.piece_size, board_coords[1] * self.square_size + self.piece_size)

    def board_coords(self, pixel):
        return (pixel[0] // self.square_size, pixel[1] // self.square_size)

    def highlight_squares(self, squares, origin):
		for square in squares:
			pygame.draw.rect(self.screen, HIGH, (square[0] * self.square_size, square[1] * self.square_size, self.square_size, self.square_size))	

		if origin != None:
			pygame.draw.rect(self.screen, HIGH, (origin[0] * self.square_size, origin[1] * self.square_size, self.square_size, self.square_size))

    def draw_message(self, message):
        self.message = True
        self.font_obj = pygame.font.Font('freesansbold.ttf', 44)
        self.text_surface_obj = self.font_obj.render(message, True, HIGH, BLACK)
        self.text_rect_obj = self.text_surface_obj.get_rect()
        self.text_rect_obj.center = (self.window_size >> 1, self.window_size >> 1)

class Board:
	def __init__(self):
		self.matrix = self.new_board()

	def new_board(self):

		matrix = [[None] * 8 for i in range(8)]

		for x in range(8):
			for y in range(8):
				if (x % 2 != 0) and (y % 2 == 0):
					matrix[y][x] = Square(WHITE)
				elif (x % 2 != 0) and (y % 2 != 0):
					matrix[y][x] = Square(BLACK)
				elif (x % 2 == 0) and (y % 2 != 0):
					matrix[y][x] = Square(WHITE)
				elif (x % 2 == 0) and (y % 2 == 0): 
					matrix[y][x] = Square(BLACK)

		for x in range(8):
			for y in range(3):
				if matrix[x][y].color == BLACK:
					matrix[x][y].occupant = Piece(RED)
			for y in range(5, 8):
				if matrix[x][y].color == BLACK:
					matrix[x][y].occupant = Piece(BLUE)

		return matrix

    def board_string(self, board):
        board_string = [[None] * 8] * 8

        for x in range(8):
            for y in range(8):
                if board[x][y].color == WHITE:
                    board_string[x][y] = "WHITE"
                else:
                    board_string[x][y] = "BLACK"

        return board_string

    def rel(self, dir, pixel):

        x = pixel[0]
        y = pixel[1]
        if dir == NORTHWEST:
            return (x - 1, y - 1)
        elif dir == NORTHEAST:
            return (x + 1, y - 1)
        elif dir ==