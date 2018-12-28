from django import forms
from .models import Post

class NewPostForm(forms.ModelForm):
	text = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 4}))
	class Meta:
		model = Post
		fields = ['title', 'text']