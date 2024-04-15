from django import forms
from .models import Symptom

class ExposureTimeForm(forms.Form):
    duration = forms.IntegerField(
        label='Your outdoor activity time',
        help_text='(in hours)',
        widget=forms.TextInput(attrs={'placeholder': 'Please enter your outdoor activity time (in hours).'}),
        label_suffix=''
    )


class SymptomForm(forms.Form):
    symptoms = forms.ModelMultipleChoiceField(
        queryset=Symptom.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )


class SymptomSelectionForm(forms.Form):
    symptoms = forms.ModelMultipleChoiceField(
        queryset=Symptom.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

class SymptomReleiferForm(forms.Form):
    symptoms = forms.ModelMultipleChoiceField(
        queryset=Symptom.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
