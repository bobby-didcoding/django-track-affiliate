# diddemo-track-affiliate

Django track affiliate is a Django app that allows you to manage affiliate programmes

Quick start:


1) Ensure you have the following packages installed

pip install pyyaml ua-parser user-agent django-user-agent geoip2

2) Add "affiliate" and "django_user_agent" to your INSTALLED_APPS setting like this.

    INSTALLED_APPS = [
        ...
        'django_user_agent',
        'django_sus',
    ]

3) Add 'django_user_agents.middleware.UserAgentMiddleware', to middleware

	MIDDLEWARE = [
    
    ...
    'django_user_agents.middleware.UserAgentMiddleware',
    ...
    
]

4) Run "python manage.py makemigrations" to create the models.

5) Run "python manage.py migrate" to migrate your new models

6) Add the following decorator to your main url i.e. home. This will create the necessary AffiliateTracker object against a session key

from affiliate.decorators import affiliate_tracker

@method_decorator(affiliate_tracker, name='dispatch')
class HomeView(TemplateView):

    template_name = "main/index.html"


7) call the AFCreate class in your sign up view

from affiliate.manager import AFCreate
def sign_up(request):

    ...
       
    #add this before calling login()
    session_key = self.request.session.session_key
                
    login(self.request, user)

    #add after calling login()
    AFCreate(request, session_key = session_key, user = user)

    ...







