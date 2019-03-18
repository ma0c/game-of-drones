import os

from django.test import TestCase

from applications.core import (
    controllers as core_controllers,
    models as core_models
)


class Loader(TestCase):

    ASSETS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

    def test_non_existing_file(self):
        self.assertRaises(
            IOError,
            core_controllers.configuration.Loader,
            ""
        )

    def test_malformed_json_file(self):
        self.assertRaises(
            ValueError,
            core_controllers.configuration.Loader,
            os.path.join(
                self.ASSETS_FOLDER,
                "malformed_json.json"
            )
        )

    def test_malformed_no_moves(self):
        self.assertRaises(
            AssertionError,
            core_controllers.configuration.Loader,
            os.path.join(
                self.ASSETS_FOLDER,
                "no_moves.json"
            )
        )

    def test_empty_loses(self):
        self.assertRaises(
            ValueError,
            core_controllers.configuration.Loader,
            os.path.join(
                self.ASSETS_FOLDER,
                "empty_loses.json"
            )
        )

    def test_all_loaded(self):
        loader = core_controllers.configuration.Loader(
            os.path.join(
                self.ASSETS_FOLDER,
                "rock_paper_scissors.json"
            )
        )
        loader.load_configuration()
        self.assertEqual(core_models.GameType.objects.all().count(), 1)
        self.assertEqual(core_models.GameMove.objects.all().count(), 3)
        self.assertEqual(core_models.MoveResult.objects.all().count(), 6)
