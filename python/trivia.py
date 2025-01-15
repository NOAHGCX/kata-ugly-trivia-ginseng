#!/usr/bin/env python3
import sys

class Game:
    def __init__(self, output_file="game_output.txt"):
        self.players = []
        self.places = [0] * 6
        self.purses = [0] * 6
        self.in_penalty_box = [0] * 6

        self.pop_questions = []
        self.science_questions = []
        self.sports_questions = []
        self.rock_questions = []

        self.current_player = 0
        self.is_getting_out_of_penalty_box = False

        for i in range(50):
            self.pop_questions.append("Pop Question %s" % i)
            self.science_questions.append("Science Question %s" % i)
            self.sports_questions.append("Sports Question %s" % i)
            self.rock_questions.append(self.create_rock_question(i))

        # Redirection de la sortie vers un fichier
        self.output_file = output_file
        self._redirect_output()

    def create_rock_question(self, index):
        return "Rock Question %s" % index

    def _redirect_output(self):
        """Redirige la sortie vers un fichier"""
        self.original_stdout = sys.stdout  # Sauvegarde la sortie d'origine
        sys.stdout = open(self.output_file, 'w')  # Redirige la sortie vers le fichier

    def _restore_output(self):
        """Restaure la sortie d'origine"""
        sys.stdout.close()  # Ferme le fichier de sortie
        sys.stdout = self.original_stdout  # Restaure sys.stdout

    def _print(self, *args, **kwargs):
        """Remplacer l'appel à print() pour écrire dans le fichier"""
        print(*args, **kwargs)

    def is_playable(self):
        return self.how_many_players >= 2

    def add(self, player_name):
        self.players.append(player_name)
        self.places[self.how_many_players] = 0
        self.purses[self.how_many_players] = 0
        self.in_penalty_box[self.how_many_players] = False

        self._print(player_name + " was added")
        self._print("They are player number %s" % len(self.players))

        return True

    @property
    def how_many_players(self):
        return len(self.players)

    def roll(self, roll):
        self._print("%s is the current player" % self.players[self.current_player])
        self._print("They have rolled a %s" % roll)

        if self.in_penalty_box[self.current_player]:
            if roll % 2 != 0:
                self.is_getting_out_of_penalty_box = True

                self._print("%s is getting out of the penalty box" % self.players[self.current_player])
                self.places[self.current_player] = self.places[self.current_player] + roll
                if self.places[self.current_player] > 11:
                    self.places[self.current_player] = self.places[self.current_player] - 12

                self._print(self.players[self.current_player] + \
                            '\'s new location is ' + \
                            str(self.places[self.current_player]))
                self._print("The category is %s" % self._current_category)
                self._ask_question()
            else:
                self._print("%s is not getting out of the penalty box" % self.players[self.current_player])
                self.is_getting_out_of_penalty_box = False
        else:
            self.places[self.current_player] = self.places[self.current_player] + roll
            if self.places[self.current_player] > 11:
                self.places[self.current_player] = self.places[self.current_player] - 12

            self._print(self.players[self.current_player] + \
                        '\'s new location is ' + \
                        str(self.places[self.current_player]))
            self._print("The category is %s" % self._current_category)
            self._ask_question()

    def _ask_question(self):
        if self._current_category == 'Pop': self._print(self.pop_questions.pop(0))
        if self._current_category == 'Science': self._print(self.science_questions.pop(0))
        if self._current_category == 'Sports': self._print(self.sports_questions.pop(0))
        if self._current_category == 'Rock': self._print(self.rock_questions.pop(0))

    @property
    def _current_category(self):
        if self.places[self.current_player] == 0: return 'Pop'
        if self.places[self.current_player] == 4: return 'Pop'
        if self.places[self.current_player] == 8: return 'Pop'
        if self.places[self.current_player] == 1: return 'Science'
        if self.places[self.current_player] == 5: return 'Science'
        if self.places[self.current_player] == 9: return 'Science'
        if self.places[self.current_player] == 2: return 'Sports'
        if self.places[self.current_player] == 6: return 'Sports'
        if self.places[self.current_player] == 10: return 'Sports'
        return 'Rock'

    def was_correctly_answered(self):
        if self.in_penalty_box[self.current_player]:
            if self.is_getting_out_of_penalty_box:
                self._print('Answer was correct!!!!')
                self.purses[self.current_player] += 1
                self._print(self.players[self.current_player] + \
                    ' now has ' + \
                    str(self.purses[self.current_player]) + \
                    ' Gold Coins.')

                winner = self._did_player_win()
                self.current_player += 1
                if self.current_player == len(self.players): self.current_player = 0

                return winner
            else:
                self.current_player += 1
                if self.current_player == len(self.players): self.current_player = 0
                return True
        else:
            self._print("Answer was correct!!!!")
            self.purses[self.current_player] += 1
            self._print(self.players[self.current_player] + \
                ' now has ' + \
                str(self.purses[self.current_player]) + \
                ' Gold Coins.')

            winner = self._did_player_win()
            self.current_player += 1
            if self.current_player == len(self.players): self.current_player = 0

            return winner

    def wrong_answer(self):
        self._print('Question was incorrectly answered')
        self._print(self.players[self.current_player] + " was sent to the penalty box")
        self.in_penalty_box[self.current_player] = True

        self.current_player += 1
        if self.current_player == len(self.players): self.current_player = 0
        return True

    def _did_player_win(self):
        return not (self.purses[self.current_player] == 6)

    def close_output(self):
        # Cette méthode permet de fermer correctement le fichier de sortie
        self._restore_output()



from random import seed, randrange



if __name__ == '__main__':
    not_a_winner = False
    seed(0)  #Ensures reproducibility of randomness

    game = Game()

    game.add('Chet')
    game.add('Pat')
    game.add('Sue')

    while True:
        game.roll(randrange(4) + 1)

        if randrange(4) == 7:
            not_a_winner = game.wrong_answer()
        else:
            not_a_winner = game.was_correctly_answered()

        if not not_a_winner: break

