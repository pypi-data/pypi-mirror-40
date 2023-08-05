from django import forms


class CommandForm(forms.Form):
    args = forms.CharField(required=False)
    automatic_noinput = forms.BooleanField(initial=True)
