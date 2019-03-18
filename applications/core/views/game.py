from django.views import generic
from django.urls import reverse_lazy
from django import http

from applications.core import (
    conf as core_conf,
    models as core_models,
    forms as core_forms,

)


class Create(generic.FormView):
    form_class = core_forms.Game
    template_name = "core/game/create.html"

    def form_valid(self, form):
        self.object = core_models.Game.objects.create(**form.cleaned_data)
        self.object.slug = core_models.Game.generate_random_slug()
        self.object.save()
        return http.HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(
            core_conf.GAME_URL_NAME,
            kwargs={
                "slug": self.object.slug,
                "pk": self.object.id
            }
        )

class Game(generic.FormView):
    form_class = core_forms.Round
    template_name = "core/game/game.html"