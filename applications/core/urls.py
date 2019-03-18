from django.urls import path

from applications.core import (
    conf
)

from applications.core.views import (
    game
)


urlpatterns = [
    path(
        '',
        game.Create.as_view(),
        name=conf.CREATE_GAME_URL_NAME
    ),
    path(
        '<int:pk>/<str:slug>',
        game.Game.as_view(),
        name=conf.GAME_URL_NAME
    )
]
