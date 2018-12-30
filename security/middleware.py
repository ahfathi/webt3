from django.contrib.sessions.models import Session
from django.http import HttpResponseForbidden
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import AnonymousUser

from security.models import RequestData, BannedIP
from users.models import User
from project import settings

class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            x_forwarded_for = request.META['HTTP_X_FORWARDED_FOR']
            request_ip = x_forwarded_for.split(',')[-1].strip()
        except:
            request_ip = request.META['REMOTE_ADDR']

        banned_ip = BannedIP.objects.filter(ip=request_ip)
        if banned_ip.exists():
            return HttpResponseForbidden(banned_ip.log)


        user_agent = request.META['HTTP_USER_AGENT']
        user = request.user
        session_key = request.session.session_key
        if user == AnonymousUser():
            user = None
        
        request_data = RequestData(ip=request_ip, user_agent=user_agent, user=user, session_key=session_key)
        request_data.save()

        if user and user.is_authenticated:
            same_user_visitors = RequestData.objects.filter(user=user).exclude(ip=request_ip)
            if same_user_visitors.count() > 0:
                Session.objects.filter(session_key__in=same_user_visitors.values_list('session_key', flat=True)).delete()
                same_user_visitors.delete()

        N = settings.REQUEST_LIMIT_NUMBER
        H = settings.REQUEST_LIMIT_TIME
        request_queryset = RequestData.objects.filter(ip=request_ip).order_by('time')
        requests = list(request_queryset)
        if len(requests) >= N:
            time_spread = requests[-1].time - requests[0].time
            if (time_spread < H):
                BannedIP.objects.create(ip=request_ip, log='sent {} requests in {} time spread.'.format(N, H))
                request_queryset.delete()
            for i in range(0, len(requests)-N+1):
                request_queryset[i].delete()

        response = self.get_response(request)

        if response.status_code == 401 or response.status_code == 403:
            request_data.authorized = False
            request_data.save()

        request_queryset = RequestData.objects.filter(ip=request_ip).order_by('time')
        requests = list(request_queryset)
        for i in range(len(requests)):
            n = 0
            while not requests[i].authorized:
                n += 1
                i += 1
            if n == N:
                BannedIP.objects.create(ip=request_ip, log='sent {} consecutive unauthorized requests.')
                request_queryset.delete()
        
        return response