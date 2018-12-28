from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import NewPostForm
from .models import Post

@login_required
def new_post(request):
	if request.method == 'POST':
		form = NewPostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return HttpResponseRedirect(request.POST['next'])
		print(form.errors)
		return HttpResponseRedirect(reverse('twitter:new_post'))
	form = NewPostForm()
	return render(request, 'twitter/new_post.html', context={'form': form})