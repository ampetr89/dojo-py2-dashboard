
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new$', views.new, name='new'),
    url(r'^edit/(?P<user_id>\d*$)', views.edit, name='edit'),
    # url(r'^update/(?P<user_id>\d+)/(?P<ud_type>\w+)$', views.update, name='update'),
    url(r'^show/(?P<user_id>\d+)', views.show, name='show'),
    url(r'^delete/(?P<user_id>\d+)', views.delete, name='delete'),
    url(r'^add_message/(?P<to_user_id>\d+)', views.add_message, name='add_message'),
]
