from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login_request', views.login_request, name='login_request'),

    url(r'^get_college_batch_years_list', views.get_college_batch_years_list, name='get_college_batch_years_list'),

    url(r'^get_all_colleges_and_universities', views.get_all_colleges_and_universities,
        name='get_all_colleges_and_universities'),

    url(r'^register_student_profile_details', views.register_student_profile_details,
        name='register_student_profile_details'),

    url(r'^get_teacher_posts', views.get_teacher_posts, name='get_teacher_posts'),

    url(r'^get_students_posts', views.get_students_posts, name='get_students_posts'),

    url(r'^get_comments_on_post', views.get_comments_on_post, name='get_comments_on_post'),

    url(r'^upvote_or_downvote_post', views.upvote_or_downvote_post, name='upvote_or_downvote_post'),

    url(r'^add_comment_on_post', views.add_comment_on_post, name='add_comment_on_post'),
    
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
    # url(r'^view_addresses', views.view_addresses, name='view_addresses'),
    # url(r'^view_addresses', views.view_addresses, name='view_addresses'),
]
