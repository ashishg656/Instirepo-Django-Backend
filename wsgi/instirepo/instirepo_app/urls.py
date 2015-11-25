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

    url(r'^save_post_for_later', views.save_post_for_later, name='save_post_for_later'),

    url(r'^get_people_who_saw_post', views.get_people_who_saw_post, name='get_people_who_saw_post'),

    url(r'^user_profile_viewed_by_other', views.user_profile_viewed_by_other, name='user_profile_viewed_by_other'),

    url(r'^upvote_or_downvote_user', views.upvote_or_downvote_user, name='upvote_or_downvote_user'),

    url(r'^get_all_post_categories', views.get_all_post_categories, name='get_all_post_categories'),

    url(r'^get_all_teachers_list', views.get_all_teachers_list, name='get_all_teachers_list'),

    url(r'^save_post_visibility', views.save_post_visibility, name='save_post_visibility'),

    url(r'^get_saved_post_visibilities', views.get_saved_post_visibilities, name='get_saved_post_visibilities'),

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
