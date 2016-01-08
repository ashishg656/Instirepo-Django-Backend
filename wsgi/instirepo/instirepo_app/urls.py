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

    url(r'^get_posts_posted_by_user', views.get_posts_posted_by_user, name='get_posts_posted_by_user'),

    url(r'^get_all_messages_list', views.get_all_messages_list, name='get_all_messages_list'),

    url(r'^get_messages_for_one_user', views.get_messages_for_one_user, name='get_messages_for_one_user'),

    url(r'^add_message_to_chats', views.add_message_to_chats, name='add_message_to_chats'),

    url(r'^add_gcm_token_for_user', views.add_gcm_token_for_user, name='add_gcm_token_for_user'),

    url(r'^block_user_request', views.block_user_request, name='block_user_request'),

    url(r'^flag_comment_on_post', views.flag_comment_on_post, name='flag_comment_on_post'),

    url(r'^get_notifications_for_user', views.get_notifications_for_user, name='get_notifications_for_user'),

    url(r'^follow_post', views.follow_post, name='follow_post'),

    url(r'^report_post', views.report_post, name='report_post'),

    url(r'^upload_post', views.upload_post, name='upload_post'),

    url(r'^upload_resume_request', views.upload_resume_request, name='upload_resume_request'),

    url(r'^delete_resume', views.delete_resume, name='delete_resume'),

    url(r'^user_profile_viewed_by_himself', views.user_profile_viewed_by_himself,
        name='user_profile_viewed_by_himself'),

    url(r'^change_email_visibility', views.change_email_visibility, name='change_email_visibility'),

    url(r'^change_phone_visibility', views.change_phone_visibility, name='change_phone_visibility'),

    url(r'^post_detail_request', views.post_detail_request, name='post_detail_request'),

    url(r'^get_posts_marked_important_by_user', views.get_posts_marked_important_by_user,
        name='get_posts_marked_important_by_user'),

    # url(r'^view_addresses', views.view_addresses, name='view_addresses'),
    # url(r'^view_addresses', views.view_addresses, name='view_addresses'),
    # url(r'^view_addresses', views.view_addresses, name='view_addresses'),
    # url(r'^view_addresses', views.view_addresses, name='view_addresses'),
    # url(r'^view_addresses', views.view_addresses, name='view_addresses'),
    # url(r'^view_addresses', views.view_addresses, name='view_addresses'),
]
