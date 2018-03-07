from django.conf.urls import url

from ubyssey.events import views

urlpatterns = [
    url(r'^$', views.events, name='events'),
    url(r'^submit/form/', views.submit_form, name='events-submit-form'),
    url(r'^submit/success/', views.submit_success, name='events-submit-success'),
    url(r'^submit/$', views.submit_landing, name='events-submit-landing'),
    url(r'^edit/success/', views.edit_success, name='events-edit-success'),
    url(r'^edit/(?P<secret_id>.+)', views.edit, name='events-edit'),
    url(r'^import/', views.event_import, name='events-import'),
    url(r'^(?P<event_id>.+)/$', views.event, name='event'),
]
