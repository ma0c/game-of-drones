from django.views import generic
from django.urls import reverse_lazy
from django import http

from applications.core import (
    conf as core_conf,
    controllers as core_controllers,
    forms as core_forms,
    models as core_models,

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


class Game(generic.FormView, generic.DetailView):
    model = core_models.Game
    form_class = core_forms.Round
    template_name = "core/game/game.html"
    context_object_name = "game"
    _game_controller = None

    def get_context_data(self, **kwargs):
        # We need to use this behavior to process in POST requests
        self.object = game = self.get_object()

        context = super(Game, self).get_context_data(**kwargs)

        self._game_controller = core_controllers.game.Game(game)
        context.update(**self._game_controller.get_game_context())
        # As we reuse this view, after post, default behavior of FormView stores data in initial property, so its
        # better just re-construct the object ignoring initial
        context['form'] = self.form_class()
        return context

    def form_valid(self, form):
        # First we load the context, to have _game_controller on current request
        context = self.get_context_data(form=form)
        self._game_controller.set_current_move(form.cleaned_data["move"])
        # The we update the context
        context.update(**self._game_controller.get_game_context())

        return self.render_to_response(context)



