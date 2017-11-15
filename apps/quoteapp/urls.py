from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^home', views.home, name='home'),
    url(r'^process_quote', views.process_quote, name='process_quote'),
    url(r'^user/(?P<user_id>\d+)$', views.profile, name = 'profile'),
    url(r'^favadd(?P<quote_id>\d+)$', views.favadd, name='favadd'),
    url(r'^favrem(?P<quote_id>\d+)$', views.favrem, name='favrem'),
]
