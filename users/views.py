from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UserChangeForm, UserCreationForm
from .models import User

from api.utils import create_token
from api.models import AccessKey

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            access_key = AccessKey(token=create_token(user), user=user)
            access_key.save()
            login(request, user)
            return HttpResponseRedirect(request.POST['next'])
        else:
            print(form.errors)
            return HttpResponseRedirect(reverse('users:register'))
    else:
        form = UserCreationForm()
        return render(request, 'users/register.html', context={'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('users:profile'))
    form = UserChangeForm(instance=request.user)
    posts = request.user.post_set.all()
    return render(request, 'users/profile.html', context={'form': form, 'posts': posts})


@login_required
def keygen(request):
    if request.method != 'GET':
        return HttpResponse('please use get method')
    token = create_token(request.user)
    user = request.user
    user.accesskey.token = token
    user.accesskey.save()
    return HttpResponseRedirect(reverse('users:profile'))
    