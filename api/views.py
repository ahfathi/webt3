from django.views import View
from django.http import JsonResponse
from users.models import User
from api.models import AccessKey
from twitter.models import Post
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from api.utils import create_token

class Login(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(Login, self).dispatch(request, *args, **kwargs)
    def post(self, request):
        json_request = json.loads(request.body)
        username = json_request.get('username')
        password = json_request.get('password')
        user = get_object_or_404(User, username=username)
        if not user.check_password(password):
            return JsonResponse({'error': 'wrong password!'})
        token = create_token(user)
        user.accesskey.token = token
        user.accesskey.save()
        return JsonResponse({'token': token})
    def get(self, request):
        return JsonResponse({'hint': 'please use post method and include your username and password in the body of your request as a json.'})

class Tweet(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(Tweet, self).dispatch(request, *args, **kwargs)
    def post(self, request):
        json_request = json.loads(request.body)
        username = json_request.get('username')
        token = json_request.get('token')
        try:
            title = json_request['title']
        except:
            return JsonResponse({'error': 'title field is required!'})
        try:
            text = json_request['text']
        except:
            return JsonResponse({'error': 'text field is required!'})
        user = get_object_or_404(User, username=username)
        if user.accesskey.token != token:
            return JsonResponse({'error': 'invalid token!'})
        new_post = Post(title=title, text=text, author=user)
        new_post.save()
        return JsonResponse({'success': 'new post added successfuly!'})
    def get(self, request):
        return JsonResponse({'hint': 'please use post method and include your username, token, title, and text in the body of your request as a json.'})