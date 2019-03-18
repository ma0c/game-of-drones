from django import forms

from applications.core import (
    models as core_models
)


class Game(forms.Form):
    player1 = forms.CharField()
    player2 = forms.CharField()

    def clean_player1(self):
        new_p1, created = core_models.Player.objects.get_or_create(name=self.cleaned_data["player1"])
        return new_p1

    def clean_player2(self):
        new_p2, created = core_models.Player.objects.get_or_create(name=self.cleaned_data["player2"])
        return new_p2

    def clean(self):
        if self.cleaned_data["player1"].id == self.cleaned_data["player2"].id:
            raise forms.ValidationError("A player cannot play against himself")
        return self.cleaned_data


class Round(forms.Form):
    move = forms.ModelChoiceField(
        queryset=core_models.GameMove.objects.all(),
        label="Select move"
    )
