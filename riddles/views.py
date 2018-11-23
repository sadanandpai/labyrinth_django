from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.cache import cache
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.contrib.auth.models import User
from riddles.models import UserDetails
from riddles.models import Answers
from django import forms
from .forms import SigninForm
from .forms import SignupForm
from .forms import AnswerForm

level_index = ['0.0', '1.1', '1.2', '1.3', '2.1', '2.2', '3.1', '4.1', '4.2', '5.1', '6.1', '7.1', '8.1', '9.1', '9.2', '10.1', '11.1', '12.1', '13.1', '13.2', '13.3', '13.4', '14.1', '15.1', '16.1', '17.1', '18.1', '19.1', '20.1', '21.1', '22.1', '23.1']
level_url = ['', 'welcome', 'who', 'answerhere', 'open', 'close', '1928', 'someoneLike', 'whatsapp', 'cryptic', 'notajackofall', 'tmbg', 'thecode', '60th', 'symbols', 'Brand', 'game', 'third', 'randomnumber', 'Sing', 'eodnhoj', 'limbo', 'jinchuriki', 'sa', 'poetry', 'eric', 'minority', 'mg', 'chel', 'ditsanddahs', 'TheFinalLevel', 'Congrats']
answer_url = ['1.1', '1.3', '2.1', '13.4']

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
			remember = request.POST.get('remember', False)
			user = authenticate(username=username, password=password)
			if user is not None:
				if remember == False:
					request.session.set_expiry(0)
				login(request, user)
				if int(user.userdetails.level) == 0:
					setuserlevel(user.id, '1.1')
				return redirect('levels')
	else:
		form = SigninForm()
	return render(request, 'html/account.html', {'form': form})

def signup(request):
	if request.user.is_authenticated:
		return redirect('/')
	elif request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			try:
				username = form.cleaned_data['signup_username']
				password = form.cleaned_data['signup_password']
				mobile = form.cleaned_data['mobile']
				email = form.cleaned_data['email']
				user = User.objects.create_user(username, email, password)
				user.userdetails.mobile = mobile
				user.save()
				return render(request, 'html/account.html')
			except Exception as e:
				return render(request, 'html/account.html', {'serverError': 'username already in use'})
	else:
		form = SignupForm()
	return render(request, 'html/account.html', {'form': form})

def about(request):
	return render(request, 'html/about.html')

def lb(request):
	context = {'users': User.objects.order_by('-userdetails__level', 'userdetails__rank')}
	return render(request, 'html/lb.html', 	context)

def logout_user(request):
	cache.set('status_%s' % (request.user.username), 0, 0)
	logout(request)
	return redirect('/')


@login_required
def levels(request):
	if request.user.userdetails.level == 0:
		setuserlevel(request.user.id, get_next_level('0.0'))
		return redirect('/levels/')
	return redirect('/levels/'+str(request.user.userdetails.level))


@login_required
def levels_quest(request, level_id):
	return redirect('/levels/'+ level_id + '/' + level_url[level_index.index(level_id)])


@login_required
def levels_quest_url(request, level_id, userlevel_url):
	if float(level_id) <= float(request.user.userdetails.level):
		if level_url[level_index.index(level_id)] == userlevel_url:
			return render(request, 'html/levels/'+level_id+'.html')
		elif level_id in answer_url:
			answer = Answers.objects.get(level=level_id)
			if userlevel_url == answer.answer:
				next_level = get_next_level(level_id)
				if float(level_id) == float(request.user.userdetails.level):
					setuserlevel(request.user.id, next_level)
					return redirect("/levels/" + next_level)
				else:
					return redirect("/levels/" + next_level)
			else:
				return redirect("/levels/" + level_id)
		else:
			return render(request, 'html/404.html')
	return render(request, 'html/404.html')


@login_required
def answers(request, level_id):
	if float(level_id) <= float(request.user.userdetails.level):
		if request.method == 'POST':
			form = AnswerForm(request.POST)
			if form.is_valid():
				useranswer = request.POST['answer']
				answer = Answers.objects.get(level=level_id)
				if useranswer == answer.answer:
					next_level = get_next_level(level_id)
					if float(level_id) == float(request.user.userdetails.level):
						setuserlevel(request.user.id, next_level)
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


def error404(request):
	return render(request, 'html/404.html')

def	setuserlevel(user_id, next_level):
	tableuser = UserDetails.objects.get(user_id = user_id)
	tableuser.level = next_level
	max_rank = UserDetails.objects.filter(level=next_level).aggregate(Max('rank'))
	if max_rank.get('rank__max') is not None:
		tableuser.rank = max_rank.get('rank__max') + 1
	else:
		tableuser.rank = 1
	tableuser.save()

def get_next_level(level_id):
	return level_index[level_index.index(level_id) + 1]
