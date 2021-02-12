from django import forms
from qa.models import Question, Answer
from django.shortcuts import get_object_or_404

class AskForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)

    def __init__(self, user, *args, **kwargs):
	self._user = user
	super(AskForm, self).__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data

    def save(self):
        self.cleaned_data['author'] = self._user
        question = Question(**self.cleaned_data)
        question.save()
        return question

class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField(widget=forms.HiddenInput)

    def clean_question(self):
        try:
            question = int(self.cleaned_data['question'])
        except ValueError:
            raise forms.ValidationError('Invalid data',
                                        code='validation_error')
        return question

    def clean(self):
        return self.cleaned_data

    def save(self):
        self.cleaned_data['question'] = get_object_or_404(Question, id=self.cleaned_data['question'])
        self.cleaned_data['author'] = self._user
        answer = Answer(**self.cleaned_data)
        answer.save
        return answer
