from django.contrib.sessions.models import Session
from django.http import HttpResponseForbidden
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import AnonymousUser

from security.models import RequestData, BannedIP
from users.models import User
from project import settings
from time import time

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
            if time() - banned_ip[0].time_banned > settings.BANNED_IP_EXPIRE_TIME:
                banned_ip.delete()
            else:
                return HttpResponseForbidden('%s %s' % (banned_ip[0].log, 'please wait {} seconds.'.format(settings.BANNED_IP_EXPIRE_TIME-int(time()-banned_ip[0].time_banned))))


        user_agent = request.META['HTTP_USER_AGENT']
        user = request.user
        session_key = request.session.session_key
        if user == AnonymousUser():
            user = None
        
        request_data = RequestData(ip=request_ip, user_agent=user_agent, user=user, session_key=session_key, time=time())
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
        delete_early_requests = False
        if len(requests) >= N:
            time_spread = requests[-1].time - requests[0].time
            if (time_spread < H):
                BannedIP.objects.create(ip=request_ip, time_banned=time(), log='sent {} requests in {} seconds.'.format(len(requests), time_spread))
                request_queryset.delete()
            else:
                delete_early_requests = True

        response = self.get_response(request)

        if response.status_code == 401 or response.status_code == 403:
            request_data.authorized = False
            request_data.save()

        request_queryset = RequestData.objects.filter(ip=request_ip).order_by('time')
        requests = list(request_queryset)
        for i in range(len(requests)):
            n = 0
            while i < len(requests) and not requests[i].authorized:
                n += 1
                i += 1
            if n >= N:
                BannedIP.objects.create(ip=request_ip, time_banned=time(), log='sent {} consecutive unauthorized requests.'.format(n))
                request_queryset.delete()
                delete_early_requests = False

        if delete_early_requests:
            for i in range(0, len(requests)-N+1):
                    request_queryset[0].delete()
        
        return response