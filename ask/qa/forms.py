from django import forms
from qa.models import Question, Answer
from django.shortcuts import get_object_or_404

class AskForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)

    def clean(self):
        return self.cleaned_data

    def save(self):
        question = Question(**self.cleaned_data)
        question.save()
        return question

class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField(widget=forms.HiddenInput)

    def clean(self):
        return self.cleaned_data

    def save(self):
        answer = Answer(**self.cleaned_data)
        answer.save()
        return answer
