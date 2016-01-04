from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^get_works_list', views.get_works_list, name='get_works_list'),

    url(r'^add_work', views.add_work, name='add_work'),

    url(r'^add_detail', views.add_detail, name='add_detail'),

    url(r'^get_details_list', views.get_details_list, name='get_details_list'),

    url(r'^delete_work', views.delete_work, name='delete_work'),
    
    # url(r'^view_addresses', views.view_addresses, name='view_addresses'),
    # url(r'^view_addresses', views.view_addresses, name='view_addresses'),
    # url(r'^view_addresses', views.view_addresses, name='view_addresses'),
    # url(r'^view_addresses', views.view_addresses, name='view_addresses'),
]
