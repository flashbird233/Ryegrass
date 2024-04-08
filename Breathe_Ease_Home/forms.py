from django import forms

class ExposureTimeForm(forms.Form):
    duration = forms.IntegerField(
        label='Your outdoor activity time',
        help_text='(in hours)',
        widget=forms.TextInput(attrs={'placeholder': 'Please enter your outdoor activity time (in hours).'}),
        label_suffix=''
    )





