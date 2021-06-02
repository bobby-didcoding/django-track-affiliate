from . models import Affiliate, Label, AffiliateTracker

class AFCreate:

    def __init__(self, request, *args, **kwargs):

        session_key = kwargs.get("session_key")
        user = kwargs.get("user")
        aid = request.session["aid"]
        label = request.session["label"]

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


        at, created = AffiliateTracker.objects.get_or_create(
                session_key = session_key
            )

        at.user = user
        if a:
            at.affiliate = a
        if l:
            at.label = l

        at.user_agent = user_agent
        at.ip_address = ip
        at.device = device
        at.log_in_count = 1
        at.save()
