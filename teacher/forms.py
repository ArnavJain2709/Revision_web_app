from django import forms


class QuestionForm(forms.Form):
    question_text = forms.CharField()
    pack = forms.IntegerField()
    option_1 = forms.CharField()
    option_2 = forms.CharField()
    option_3 = forms.CharField()
    option_4 = forms.CharField()
    correct_option = forms.IntegerField(min_value=1, max_value=4)
