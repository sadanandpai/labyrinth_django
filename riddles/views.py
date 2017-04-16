from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.signing import Signer

from django.contrib.auth.models import User
from riddles.models import UserDetails
from riddles.models import Answers
from django import forms
from .forms import SigninForm
from .forms import SignupForm
from .forms import AnswerForm


level_index = ['1', '2', '3', '4', '5']

def index(request):
	return render(request, 'html/index.html')


def signin(request):
	if request.user.is_authenticated:
		return redirect('/')
	elif request.method == 'POST':
		form = SigninForm(request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('levels')
	else:
		form = SigninForm()
	return render(request, 'html/account.html', {'form': form})


def signup(request):
	if request.user.is_authenticated is not None:
		return redirect('/')
	elif request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['signup_username']
			password = form.cleaned_data['signup_password']
			mobile = form.cleaned_data['mobile']
			email = form.cleaned_data['email']
			user = User.objects.create_user(username, email, password)
			user.userdetails.mobile = mobile
			user.save()
	else:
		form = SignupForm()
	return render(request, 'html/account.html', {'form': form})


def logout_user(request):
	logout(request)
	return redirect('/')


@login_required
def levels(request):
	return redirect('/levels/'+ str(request.user.userdetails.level))

@login_required
def levels_quest(request, level_id):
	if int(level_id) <= request.user.userdetails.level:
		return render(request, 'html/levels/'+level_id+'.html')
	else:
		return render(request, 'html/404.html')

@login_required
def answers(request, level_id):
	if int(level_id) <= request.user.userdetails.level:
		if request.method == 'POST':
			form = AnswerForm(request.POST)
			if form.is_valid():
				useranswer = request.POST['answer']
				answer = Answers.objects.get(level=level_id)
				if useranswer == answer.answer:
					next_level = get_next_level(level_id)
					if int(level_id) == request.user.userdetails.level:
						tableuser = UserDetails.objects.get(user_id = request.user.id)
						tableuser.level = next_level
						tableuser.save()
						return redirect("/levels/" + next_level)
					else:
						return redirect("/levels/" + next_level)
				else:
					return redirect("/levels/" + level_id)
			else:
				return redirect("/levels/" + level_id)
		else:
			return render(request, 'html/404.html')
	else:
		return render(request, 'html/404.html')


@login_required
def answers_url(request, level_id, useranswer):
	if int(level_id) <= request.user.userdetails.level:
		if request.method == 'GET':
			answer = Answers.objects.get(level=level_id)
			if useranswer == answer.answer:
				next_level = get_next_level(level_id)
				if int(level_id) == request.user.userdetails.level:
					tableuser = UserDetails.objects.get(user_id = request.user.id)
					tableuser.level = get_next_level(level_id)
					tableuser.save()
					return redirect("/levels/" + next_level)
				else:
					return redirect("/levels/" + next_level)
			else:
				return redirect("/levels/" + level_id)
		else:
			return render(request, 'html/404.html')
	else:
		return render(request, 'html/404.html')


def get_next_level(level_id):
	return level_index[level_index.index(level_id) + 1]