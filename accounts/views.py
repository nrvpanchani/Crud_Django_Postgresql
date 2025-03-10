from django.shortcuts import render, redirect
from django.contrib	.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.models import User, auth
from .forms import UserLoginForm, UserRegistrationForm
# Create your views here.
def login_view(request):
	next = request.GET.get('next')
	title = "Login"
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username, password=password)
		login(request, user)
		if next:
			return redirect(next)
		return redirect("/")
	return render(request, "forms.html", {"form":form, "title":title})

def registration_view(request):
	next = request.GET.get('next')
	title = "Registration"
	form = UserRegistrationForm(request.POST or None)
	if form.is_valid():
		#user = form.save(commit=False)
		username = form.cleaned_data['username']
		email = form.cleaned_data['email']
		password = form.cleaned_data['password']
		User.objects.create_user(username=username, email=email, password=password)
		user = authenticate(username=username, password=password)
		login(request, user)
		if next:
			return redirect(next)
		return redirect("/")
	context = {
		"form": form,
		"title": title
	}
	return render(request, "forms.html", context)

def logout_view(request):
	logout(request)
	return redirect("/")