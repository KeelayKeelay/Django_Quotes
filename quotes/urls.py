from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include("apps.quoteapp.urls", namespace = 'quoteapp')),
    url(r'^', include("apps.login.urls", namespace = 'login')),
]
