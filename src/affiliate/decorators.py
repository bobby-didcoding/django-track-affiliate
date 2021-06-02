from . models import Affiliate, Label, AffiliateTracker
from django.contrib.auth.models import User
from functools import wraps

def affiliate_tracker(function):
    '''
    Handels AID & Label if passed through and creates a new AffiliateTracker object
    '''
    @wraps(function)
    def wrap(request, *args, **kwargs):

        session = request.session
        session.modified = True
        session.save()
        session_key = request.session.session_key

        aid = request.GET.get("aid", None)
        label = request.GET.get("label", None)

        if aid:
            session["aid"] = aid
            session.save()
        if label:
            session["label"] = label
            session.save()

        try:
            a = Affiliate.objects.get(aid = aid)
        except Affiliate.DoesNotExist:
            a = None

        try:
            l = Label.objects.get(label = label)
        except Label.DoesNotExist:
            l = None

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        user_agent = request.user_agent
        device = f'{request.user_agent.browser.family} on {request.user_agent.device.family}'

        if a and l: 
            at = AffiliateTracker.objects.create(
                    session_key = session_key,
                    affiliate = a,
                    label = l,
                    user_agent = user_agent,
                    device = device,
                    ip_address = ip
                )

        return function(request, *args, **kwargs)

    return wrap