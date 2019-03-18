from django.test import TestCase

from applications.core import (
    controllers as core_controllers,
    models as core_models

)


class Game(TestCase):
    _game = None
    _p1 = None
    _p2 = None
    _rock_move = None
    _scissors_move = None

    def setUp(self):
        configuration = core_controllers.configuration.Loader("rock_paper_scissors.json")
        configuration.load_configuration()
        self._p1 = core_models.Player.objects.create(name="P1")
        self._p2 = core_models.Player.objects.create(name="P2")
        self._game = core_models.Game.objects.create(
                player1=self._p1,
                player2=self._p2,
        )
        self._rock_move = core_models.GameMove.objects.get(name="rock")
        self._scissors_move = core_models.GameMove.objects.get(name="scissors")

    def test_new_game(self):
        game_controller = core_controllers.game.Game(self._game)
        context = game_controller.get_game_context()

        self.assertEqual(context["current_player"], self._p1)
        self.assertEqual(len(context["rounds"]), 0)

    def test_player_switching(self):
        game_controller = core_controllers.game.Game(self._game)
        # Execute the first initialization
        game_controller.get_game_context()
        game_controller.set_current_move(self._rock_move)
        context = game_controller.get_game_context()
        # Switch to p2
        self.assertEqual(context["current_player"], self._p2)
        game_controller.set_current_move(self._rock_move)
        # Switch to p1
        self.assertEqual(context["current_player"], self._p2)

    def test_win_movement(self):
        game_controller = core_controllers.game.Game(self._game)
        # Execute the first initialization
        game_controller.get_game_context()
        game_controller.set_current_move(self._rock_move)
        # Update game
        game_controller.get_game_context()
        game_controller.set_current_move(self._scissors_move)
        context = game_controller.get_game_context()
        # Check P1 Win battle
        self.assertEqual(context["rounds"][0]["status"], self._p1)

    def test_tie_movement(self):
        game_controller = core_controllers.game.Game(self._game)
        # Execute the first initialization
        game_controller.get_game_context()
        game_controller.set_current_move(self._rock_move)
        # Update game
        game_controller.get_game_context()
        game_controller.set_current_move(self._rock_move)
        context = game_controller.get_game_context()
        # Check battle is a tie
        self.assertEqual(context["rounds"][0]["status"], "Tie")

    def test_emperor(self):
        game_controller = core_controllers.game.Game(self._game)
        # Execute the first initialization
        game_controller.get_game_context()
        # P1 Wins 3 times
        for _ in range(3):
            game_controller.set_current_move(self._rock_move)
            # Update game
            game_controller.get_game_context()
            game_controller.set_current_move(self._scissors_move)
            game_controller.get_game_context()
        # Check battle is a tie
        self.assertEqual(self._game.winner, self._p1)
