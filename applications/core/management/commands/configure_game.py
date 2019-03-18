from django.core.management import base


from applications.core import (
    controllers as core_controllers
)


class Command(base.BaseCommand):
    """
    Use this class to interact with the configuration of the game
    """
    help = "Load a configuration for the Game"

    def add_arguments(self, parser):
        parser.add_argument('path')

    def handle(self, *args, **options):
        configuration_controller = core_controllers.configuration.Loader(options["path"])
        configuration_controller.load_configuration()
