import random

import pygame
from keras.src.saving import load_model

from gomoku import Gomoku
import gomoku.mcts
from gomoku.palette import COLOR_BLACK, COLOR_RED, COLOR_GRAY, COLOR_GREEN, COLOR_WHITE
import numpy as np

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    stone = {}
    stone["white"], stone["black"] = [], []
    player1_score, player2_score = 0, 0
    game = Gomoku()  # instantiates the game, which draws out the board and sets the scores
    game.draw_main()
    game.draw_score(player1_score, player2_score)
    m1 = load_model('/Users/25yoon/PycharmProjects/magister/gomoku/img/models/20201213_202430.h5')

    play_order = True  # Start with player's turn
    def get_ai_move_again(board_state):
        new_board_state = np.pad(board_state, ((2,3), (2,3)), mode = 'constant', constant_values = 0)
        res = new_board_state.reshape(1,20,20,1)
        y_pred = m1.predict(res).squeeze()  # get rid of that one dimension
        y_pred = y_pred.reshape(20, 20)
        x, y = np.unravel_index(np.argmax(y_pred), y_pred.shape)
        return int(45 + (45 * x)),int(45 + (45 * y))

    def check_win(stone, color, player_score, player_order):
        print('run check win method')
        """
        Checks if a player has won by examining the current board state.
        """
        # Implement the win-checking logic based on the current board (stone dict)
        # It should check if there are 5 consecutive stones of the same color.
        # For now, let's assume you have such a method implemented.
        return game.score(stone, color, player_score, player_order)[2]  # Example, modify as needed

    def reset_game():
        """
        Resets the game board for the next round.
        """
        stone["white"], stone["black"] = [], []
        game.draw_main()
        game.draw_score(player1_score, player2_score)

    while True:
        event = pygame.event.poll()
        if event.type == pygame.MOUSEBUTTONDOWN:

            x_stone, y_stone = game.play_get_pos()

            # New game reset
            if (125 + 45 * 16) > x_stone > 45 * 16 and 90 > y_stone > 45:
                stone["white"], stone["black"] = [], []
                player1_score, player2_score = 0, 0
                game = Gomoku()
                game.draw_main()
                game.draw_score(player1_score, player2_score)
                game.text_draw("GAME START", game.w_h // 2, 30, COLOR_GREEN, 35)
                play_order = True
                print(play_order)
                print("game start")
                board_state = np.zeros((15, 15))

            # If player is trying to place a stone.
            if 45 <= x_stone <= game.w_h and 45 <= y_stone <= game.w_h:

                if play_order:  # Player 1's turn (white stone)
                    print("==============\n" + 'human turn')
                    x_stone, y_stone = game.play_draw_stone_pos()
                    stone, play_order = game.play_draw_stone(
                        stone, play_order, "white", COLOR_WHITE, x_stone, y_stone
                    )
                    print(str(play_order) + 'why')
                    print('p1')
                    print(x_stone, y_stone)
                    board_state[int((x_stone - 45) / 45)][int((y_stone - 45) / 45)] = 1


                    if check_win(stone, "white", player1_score, play_order):
                        print('1 won')
                        player1_score += 1
                        game.text_draw("PLAYER 1 WINS!", 45 * 16 + 65, game.w_h // 2 + 120, COLOR_RED, 45)
                        game.draw_score(player1_score, player2_score)
                        reset_game()
                    print(play_order)


                else:  # AI's turn (black stone)
                    print('====================\n'  +  'AI turn ')


                    #best_move = gomoku.mcts.mcts_ai_make_move(game, stone, play_order, num_simulations=100)#(random.randint(90, 500), random.randint(90,500)) #gomoku.mcts.mcts_ai_make_move(game, stone, play_order, num_simulations=100)
                    best_move = get_ai_move_again(board_state)
                    print(str(best_move))
                    if best_move is not None:
                        x_stone, y_stone = best_move
                        print('seq 1')
                        stone, play_order = game.play_draw_stone(
                            stone, play_order, "black", COLOR_BLACK, x_stone, y_stone
                        )
                        print('seq 2')
                        print(play_order)
                        print('p2')
                        board_state[int((x_stone - 45) / 45)][int((y_stone - 45) / 45)] = -1

                        if check_win(stone, "black", player2_score, play_order):
                            player2_score += 1
                            game.text_draw("PLAYER 2 WINS!", 45 * 16 + 65, game.w_h // 2 + 120, COLOR_RED, 45)
                            game.draw_score(player1_score, player2_score)
                            reset_game()

                # Check if it's a draw (if board is full)
                if len(stone["white"]) + len(stone["black"]) == 225:
                    game.text_draw("DRAW", 45 * 16 + 65, game.w_h // 2 + 120, (200, 0, 0), 45)
                    reset_game()

        game.interactive_button()
        pygame.display.update()

