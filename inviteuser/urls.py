from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^accept-invite/(?P<key>\w+)/?$', views.AcceptInvite.as_view(),
        name='accept-invite'),
    url(r'^accept-invite-error/$', views.AcceptErrorView.as_view(),
        name='accept-invite-error'),
]
