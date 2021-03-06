from django import forms
from .models import User

class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('username', 'nickname', 'password1', 'password2')

	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super().save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user

class UserChangeForm(forms.ModelForm):
	access_key = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'disabled': True, 'size': 90}))
	class Meta:
		model = User
		fields = ('username', 'nickname', 'email', 'avatar', 'access_key')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.fields['access_key'].initial = self.instance.accesskey.token
		for field in self.Meta.fields:
			self.fields[field].required = False

