''' This is the main logic for a Tic-tac-toe game.
It is not optimised for a quality game it simply
generates random moves and checks the results of
a move for a winning line. Exposed functions are:
newGame()
saveGame()
restoreGame()
userMove()
computerMove()
'''

import os, random
import oxo_data

class OxoGame:
    def __init__(self, game=None):
        if game and len(game) == 9:
            self.game = game
        else:
            self.game = [" "] * 9

    @classmethod
    def restore(cls):
        try:
            game = oxo_data.restoreGame()
            return cls(game)
        except IOError:
            return cls()

    def save(self):
        oxo_data.saveGame(self.game)

    def _generate_move(self):
        options = [i for i, cell in enumerate(self.game) if cell == " "]
        return random.choice(options) if options else -1

    def _is_winning_move(self):
        wins = ((0,1,2), (3,4,5), (6,7,8),
                (0,3,6), (1,4,7), (2,5,8),
                (0,4,8), (2,4,6))
        for a, b, c in wins:
            chars = self.game[a] + self.game[b] + self.game[c]
            if chars == 'XXX' or chars == 'OOO':
                return True
        return False

    def user_move(self, cell):
        if self.game[cell] != ' ':
            raise ValueError('Invalid cell')
        self.game[cell] = 'X'
        return 'X' if self._is_winning_move() else ""

    def computer_move(self):
        cell = self._generate_move()
        if cell == -1:
            return 'D'
        self.game[cell] = 'O'
        return 'O' if self._is_winning_move() else ""

    def is_draw(self):
        return " " not in self.game

    def __str__(self):
        return str(self.game)

def test():
    result = ""
    game = OxoGame()
    while not result:
        print(game)
        try:
            result = game.user_move(game._generate_move())
        except ValueError:
            print("Oops, that shouldn't happen")
        if not result:
            result = game.computer_move()
        if not result:
            continue
        elif result == 'D':
            print("Its a draw")
        else:
            print("Winner is:", result)
        print(game)

if __name__ == "__main__":
    test()