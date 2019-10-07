from django import forms
from django.contrib.auth import authenticate, get_user_model, login, logout
User = get_user_model()

class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		#user_qs = User.objects.filter(username=username)
		#if user_qs.count() == 1:
		#	user = user_qs.first()
		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("This user does not exist")

			if not user.check_password(password):
				raise forms.ValidationError("Incorrect Password")

			if not user.is_active:
				raise forms.ValidationError("This user is not longer active")

		return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegistrationForm(forms.Form):
	email = forms.EmailField(label="Email address",widget=forms.EmailInput)
	username = forms.CharField()
	password = forms.CharField(label="Password",widget=forms.PasswordInput)
	password2 = forms.CharField(label="Confirm Password",widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = ['email','username','password','password2']

	def clean_email(self):
		email = self.cleaned_data.get("email")
		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("Email already exist")

		return email

	def clean_password2(self):
		password = self.cleaned_data.get("password")
		password2 = self.cleaned_data.get("password2")
		if password != password2:
			raise forms.ValidationError("Password must match")

		return password
