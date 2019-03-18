from typing import List

from applications.core import (
    models as core_models
)


class Game(object):
    _game = None
    _current_player = None
    _current_round = None
    _rounds = None

    def __init__(self, game: core_models.Game):
        self._game = game

    def _create_new_round(self):
        self._current_round = core_models.Round.objects.create(
            game=self._game,
            number=self._rounds.count() + 1
        )
        self._game.current_round = self._rounds.count()
        self._game.save()

    def get_game_context(self):
        context = dict()
        self._rounds = self._game.round_set.order_by("-number")
        # The game just begins
        if self._rounds.count() == 0:
            self._create_new_round()
            self._current_player = self._game.player1
        else:
            self._current_round = self._rounds.first()
            # If the player 2 has played, we create a new round
            if self._current_round.player2_move is not None:
                self._create_new_round()
                self._current_player = self._game.player1
            else:
                self._current_player = self._game.player2 if self._current_round.player1_move is not None else self._game.player1
        context["current_player"] = self._current_player
        context["rounds"] = self.calculate_score()
        return context

    def set_current_move(self, move):
        if self._current_player == self._game.player1:
            self._current_round.player1_move = move
        else:
            self._current_round.player2_move = move
        self._current_round.save()

    def calculate_score(self):
        score = list()
        game_state = list()
        for round in self._rounds:
            if round.player1_move is not None and round.player2_move is not None:
                current_round = {
                    "number": round.number,
                }
                if round.player1_move == round.player2_move:
                    current_round["status"] = "Tie"
                else:
                    try:
                        move_result = core_models.MoveResult.objects.get(
                            move=round.player1_move,
                            against=round.player2_move
                        )
                        if move_result.wins:
                            current_round["status"] = round.game.player1
                            game_state.append(1)
                        else:
                            current_round["status"] = round.game.player2
                            game_state.append(-1)
                    except core_models.MoveResult.DoesNotExist:
                        current_round["status"] = "Unknown result"
                score.append(current_round)
        p1_wins = game_state.count(1)
        p2_wins = game_state.count(-1)
        # This is ugly hardcoded, but I was getting out of time
        if p1_wins >= 3:
            self._game.winner = self._game.player1
            self._game.save()
        if p2_wins >= 3:
            self._game.winner = self._game.player2
            self._game.save()

        return score
