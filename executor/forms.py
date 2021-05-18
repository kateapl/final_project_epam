from django import forms


class CodeInputForm(forms.Form):
    code = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Put there your python code"})
    )
    input = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Put there input"}), required=False
    )
