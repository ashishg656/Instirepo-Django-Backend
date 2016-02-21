from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^get_all_product_categories_and_trending_and_recent_products',
        views.get_all_product_categories_and_trending_and_recent_products,
        name='get_all_product_categories_and_trending_and_recent_products'),

    url(r'^get_products_from_category', views.get_products_from_category, name='get_products_from_category'),

    url(r'^get_trending_products', views.get_trending_products, name='get_trending_products'),

    url(r'^get_recent_products', views.get_recent_products, name='get_recent_products'),

    url(r'^get_product_detail', views.get_product_detail, name='get_product_detail'),

    url(r'^get_comments_on_product', views.get_comments_on_product, name='get_comments_on_product'),

    url(r'^add_comment_on_product', views.add_comment_on_product, name='add_comment_on_product'),

    url(r'^flag_comment_on_product', views.flag_comment_on_product, name='flag_comment_on_product'),

    url(r'^save_product_for_later', views.save_product_for_later, name='save_product_for_later'),

    # url(r'^view_addresses', views.view_addresses, name='view_addresses'),
    # url(r'^view_addresses', views.view_addresses, name='view_addresses'),
    # url(r'^view_addresses', views.view_addresses, name='view_addresses'),
    # url(r'^view_addresses', views.view_addresses, name='view_addresses'),
    # url(r'^view_addresses', views.view_addresses, name='view_addresses'),
    # url(r'^view_addresses', views.view_addresses, name='view_addresses'),
    # url(r'^view_addresses', views.view_addresses, name='view_addresses'),
    # url(r'^view_addresses', views.view_addresses, name='view_addresses'),
    # url(r'^view_addresses', views.view_addresses, name='view_addresses'),
    # url(r'^view_addresses', views.view_addresses, name='view_addresses'),
    # url(r'^view_addresses', views.view_addresses, name='view_addresses'),
]
