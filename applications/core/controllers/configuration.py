import json

from applications.core import (
    models as core_models
)


class Loader(object):
    _config = None
    _valid_moves = None

    def __init__(self, path):
        try:
            with open(path) as f:
                self._config = json.load(f)
        except IOError:
            raise IOError(f"Problem reading file {path}")
        except ValueError:
            raise ValueError("Malformed JSON")
        self.validate_configuration()

    def validate_configuration(self):
        # We want to be sure the configuration is valid
        try:
            assert self._config["name"]
            assert self._config["moves"]
            assert isinstance(self._config["moves"], list) and len(self._config["moves"]) > 0
        except (AssertionError, KeyError) as e:
            raise AssertionError("Misconfigured JSON, needs to have a name and a name and moves")

        # We will store all valid moves first and then evaluate all wins and loses
        self._valid_moves = list()
        for move in self._config["moves"]:
            try:
                assert move["name"]
                assert move["wins"]
                assert move["loses"]
                assert isinstance(move["wins"], list) and len(move["wins"]) > 0
                assert isinstance(move["loses"], list) and len(move["loses"]) > 0
                self._valid_moves.append(move["name"])
            except AssertionError:
                raise ValueError(f"{move} needs to have a name, and a non empty lists for wins and loses")

        for move in self._config["moves"]:
            for win in move["wins"]:
                if win not in self._valid_moves:
                    raise ValueError(f"{win} is not a valid move")

            for loss in move["loses"]:
                if loss not in self._valid_moves:
                    raise ValueError(f"{loss} is not a valid move")

    def load_configuration(self):
        game_type = core_models.GameType.objects.create(
            name=self._config["name"]
        )
        # We create all moves and store in a dict for easy acces in move result stage
        cache_moves = dict()
        for move in self._valid_moves:
            cache_moves[move] = core_models.GameMove.objects.create(
                game_type=game_type,
                name=move
            )

        for move in self._config["moves"]:
            for win in move["wins"]:
                core_models.MoveResult.objects.create(
                    game_type=game_type,
                    move=cache_moves[move["name"]],
                    against=cache_moves[win],
                )
            for loses in move["loses"]:
                core_models.MoveResult.objects.create(
                    game_type=game_type,
                    move=cache_moves[move["name"]],
                    against=cache_moves[loses],
                    wins=False
                )

