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
	question.author_id = self._user.id
        question.save()
        return question

class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField(widget=forms.HiddenInput)

    def clean_question(self):
	question_id = self.cleaned_data['question']
	try:
	    question = Question.objects.get(id=question_id)
	except Question.DoesNotExist:
	    question = None

    def clean(self):
        return self.cleaned_data

    def save(self):
        answer = Answer(**self.cleaned_data)
	answer.author_id = self._user.id
        answer.save()
        return answer
