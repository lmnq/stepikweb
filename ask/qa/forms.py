from django import forms
from qa.models import Question, Answer
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


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

class SignupForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
	username = self.cleaned_data['username']
	if username.strip() == '':
	    raise forms.ValidationError('Username is empty')
	return username

    def clean_email(self):
	email = self.cleaned_data['email']
	if email.strip() == '':
	    raise forms.ValidationError('Email is empty')
	return email

    def clean_password(self):
	password = self.cleaned_data['password']
	if password.strip() == '':
	    raise forms.ValidationError('Password is empty')
	return password

    def save(self):
	user = User.objects.create_user(**self.cleaned_data)
	user.save()
	auth = authenticate(**self.cleaned_data)
	return auth


class LoginForm(forms.Form):
    username = forms.Charfield(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        if username.strip() == '':
            raise forms.ValidationError('Username is empty') 
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if password.strip() == '':
            raise forms.ValidationError('Password is empty')
        return password

    def save(self):
	auth = authenticate(**self.cleaned_data)
	return auth
