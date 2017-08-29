from django.conf.urls import url

from ubyssey.events import views

urlpatterns = [
    url(r'^$', views.events, name='events'),
    url(r'^(?P<event_id>[0-9]+)/$', views.event, name='event'),
    url(r'^submit/form/', views.submit_form, name='events-submit-form'),
    url(r'^submit/success/', views.submit_success, name='events-submit-success'),
    url(r'^submit/$', views.submit_landing, name='events-submit-landing'),
]
