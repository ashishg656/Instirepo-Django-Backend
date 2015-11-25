from ctypes import c_short
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest, Http404, JsonResponse
from django.shortcuts import render, redirect
from PIL import Image
from django.template import RequestContext
from django.template.context_processors import request
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.core import serializers
import json
import requests
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from instirepo_web.models import *
from django.core import serializers
from push_notifications.models import GCMDevice
from django.db.models import Q


@csrf_exempt
def login_request(request):
    access_token = request.POST.get('access_token')
    user_id = request.POST.get('user_id')
    profile_object = request.POST.get('additional_data')
    email = request.POST.get('email')
    name = request.POST.get('name')
    image_url = request.POST.get('image_url')

    username = str(email) + str(user_id)
    password = user_id
    if len(username) > 30:
        username = username[0:29]

    is_details_found_on_server = False

    user = authenticate(username=username, password=password)
    if user is not None:
        user_profile = user.user_profile.get()
        user_profile.access_token = access_token
        user_profile.profile_details_json_object = profile_object
        user_profile.profile_image = image_url
        user_profile.save()
        if user_profile.has_provided_college_details:
            is_details_found_on_server = True
    else:
        user = User.objects.create_user(username, str(email), password)
        user.first_name = str(name)
        user.save()
        user_profile = UserProfiles(user_obj=user, full_name=name, userIDAuth=user_id, access_token=access_token,
                                    profile_details_json_object=profile_object, profile_image=image_url)
        user_profile.save()

    user_id_to_send = user.id

    return JsonResponse({'user_id': user_id_to_send, 'is_details_found_on_server': is_details_found_on_server})


@csrf_exempt
def get_all_colleges_and_universities(request):
    colleges_list = []
    university_list = []

    universities = Universities.objects.all()
    for univ in universities:
        university_list.append({'name': univ.name, 'location': univ.location, 'id': univ.id})
        colleges = univ.college_set.all()
        for coll in colleges:
            colleges_list.append(
                {'university_id': univ.id, 'name': coll.name, 'location': coll.location, 'id': coll.id})

    return JsonResponse({'colleges_list': colleges_list, 'university_list': university_list})


@csrf_exempt
def get_college_batch_years_list(request):
    college_id = request.POST.get('college_id')
    college = None
    try:
        college = College.objects.get(pk=int(college_id))
    except:
        user_id = request.POST.get('user_id')
        user_profile = User.objects.get(pk=int(user_id)).user_profile.get()
        college = user_profile.college

    branches_list = []
    years_list = []
    batches_list = []

    branches = Branches.objects.filter(college=college)
    for branch in branches:
        branches_list.append({'branch_name': branch.branch_name, 'branch_id': branch.id})
        years = branch.studentyears_set.all()
        for year in years:
            years_list.append(
                {'branch_id': branch.id, 'year_name': year.year_name, 'admission_year': year.admission_year,
                 'passout_year': year.passout_year, 'has_passed_out': year.has_passed_out, 'year_id': year.id})
            batches = year.batches_set.all()
            for batch in batches:
                batches_list.append({'year_id': year.id, 'batch_name': batch.batch_name, 'batch_id': batch.id})

    return JsonResponse({'branches_list': branches_list, 'years_list': years_list, 'batches_list': batches_list})


@csrf_exempt
def register_student_profile_details(request):
    university_id_req = request.POST.get('university_id')
    college_id_req = request.POST.get('college_id')
    enrollment_number_req = request.POST.get('enrollment_number')
    branch_id_req = request.POST.get('branch_id')
    year_id_req = request.POST.get('year_id')
    batch_id_req = request.POST.get('batch_id')
    user_id = request.POST.get('user_id')

    user = User.objects.get(pk=int(user_id))
    profile = user.user_profile.get()

    profile.enrollment_number = enrollment_number_req
    profile.has_provided_college_details = True
    profile.college = College.objects.get(pk=int(college_id_req))
    profile.batch = Batches.objects.get(pk=int(batch_id_req))
    profile.branch = Branches.objects.get(pk=int(branch_id_req))
    profile.university = Universities.objects.get(pk=int(university_id_req))
    profile.year = StudentYears.objects.get(pk=int(year_id_req))

    profile.save()

    return JsonResponse({'error': False})


@csrf_exempt
def get_teacher_posts(request):
    user_id = request.POST.get('user_id')
    user_id = int(user_id)
    pagenumber = request.GET.get('pagenumber', 1)

    user = User.objects.get(pk=user_id)
    user_profile = user.user_profile.get()

    teacher_posts = []
    query = Posts.objects.filter((Q(is_by_teacher=True))).order_by('-time')

    query_paginated = Paginator(query, 20)
    query = query_paginated.page(pagenumber)
    next_page = None
    if query.has_next():
        next_page = query.next_page_number()

    for post in query:
        temp = User.objects.get(pk=int(post.uploader.id)).user_profile.get()
        image = None
        try:
            image = post.image.url
        except:
            pass
        upvotes = UpvotesOnPosts.objects.filter(is_upvote=True, is_active=True, post=post).count()
        downvotes = UpvotesOnPosts.objects.filter(is_upvote=False, is_active=True, post=post).count()
        has_upvoted = UpvotesOnPosts.objects.filter(is_upvote=True, is_active=True, post=post, user=user).count()
        has_downvoted = UpvotesOnPosts.objects.filter(is_upvote=False, is_active=True, post=post, user=user).count()
        seens = PostSeens.objects.filter(post=post).count()
        saves = SavedPosts.objects.filter(post=post, is_active=True).count()
        is_saved = SavedPosts.objects.filter(post=post, user=user, is_active=True).count()
        category = post.category.name
        category_color = post.category.color

        has_downvoted = getBooleanFromQueryCount(has_downvoted)
        has_upvoted = getBooleanFromQueryCount(has_upvoted)
        is_saved = getBooleanFromQueryCount(is_saved)

        comment = CommentsOnPosts.objects.filter(post=post).count()

        teacher_posts.append(
            {'id': post.id, 'heading': post.heading, 'description': post.description, 'image': image, 'time': post.time,
             'user_image': temp.profile_image, 'user_name': temp.full_name, 'upvotes': upvotes, 'downvotes': downvotes,
             'has_upvoted': has_upvoted, 'has_downvoted': has_downvoted, 'comment': comment, 'seens': seens,
             'category': category, 'category_color': category_color, 'saves': saves, 'is_saved': is_saved,
             'user_id': post.uploader.id})

    return JsonResponse({'posts': teacher_posts, 'next_page': next_page})


@csrf_exempt
def save_post_for_later(request):
    user_id = request.POST.get('user_id')
    post_id = request.POST.get('post_id')

    post = Posts.objects.get(pk=int(post_id))
    user = User.objects.get(pk=int(user_id))

    is_saved = True
    try:
        query = SavedPosts.objects.get(post=post, user=user)
        if query.is_active:
            query.is_active = False
            is_saved = False
        else:
            query.is_active = True
        query.save()
    except:
        query = SavedPosts(post=post, user=user)
        query.save()

    count = SavedPosts.objects.filter(post=post, is_active=True).count()

    return JsonResponse({'count': count, 'is_saved': is_saved})


@csrf_exempt
def get_comments_on_post(request):
    pagenumber = request.GET.get('pagenumber', 1)
    user_id = request.POST.get('user_id')
    post_id = request.GET.get('post_id')

    post = Posts.objects.get(pk=int(post_id))

    query = CommentsOnPosts.objects.filter(post=post, is_active=True).order_by('-time')
    count = CommentsOnPosts.objects.filter(post=post, is_active=True).count()

    query_paginated = Paginator(query, 20)
    query = query_paginated.page(pagenumber)
    next_page = None
    if query.has_next():
        next_page = query.next_page_number()

    comments = []
    for comment in query:
        is_by_user = False
        if comment.user.id == int(user_id):
            is_by_user = True
        temp_user = UserProfiles.objects.get(user_obj=comment.user)
        user_name = temp_user.full_name
        user_image = temp_user.profile_image
        is_different_color = False
        if temp_user.is_senior_professor or temp_user.is_professor:
            is_different_color = True
        comments.append({'id': comment.id, 'comment': comment.comment, 'time': comment.time, 'user_name': user_name,
                         'user_image': user_image, 'is_by_user': is_by_user, 'is_different_color': is_different_color})

    return JsonResponse({'comments': comments, 'next_page': next_page, 'count': count})


@csrf_exempt
def add_comment_on_post(request):
    user_id = request.POST.get('user_id')
    post_id = request.POST.get('post_id')
    comment = request.POST.get('comment')

    user = User.objects.get(pk=int(user_id))
    post = Posts.objects.get(pk=int(post_id))
    user_profile = user.user_profile.get()

    query = CommentsOnPosts(comment=comment, user=user, post=post)
    query.save()

    count = CommentsOnPosts.objects.filter(post=post, is_active=True).count()

    return JsonResponse(
        {'count': count, 'id': query.id, 'name': user_profile.full_name, 'image': user_profile.profile_image})


@csrf_exempt
def upvote_or_downvote_post(request):
    user_id = request.POST.get('user_id')
    post_id = request.POST.get('post_id')
    is_upvote_clicked = request.POST.get('is_upvote_clicked')
    is_upvote_clicked = parseBoolean(is_upvote_clicked)

    user = User.objects.get(pk=int(user_id))
    post = Posts.objects.get(pk=int(post_id))

    message = None

    try:
        query = UpvotesOnPosts.objects.get(user=user, post=post)
        if query.is_active:
            if query.is_upvote and is_upvote_clicked:
                message = "Already upvoted and clicked on upvote"
            elif query.is_upvote and not is_upvote_clicked:
                query.is_active = False
                message = "Earlier upvoted but now no vote"
            elif not query.is_upvote and is_upvote_clicked:
                query.is_active = False
                message = "Earlier downvoted but now no vote"
            elif not query.is_upvote and not is_upvote_clicked:
                message = "Already downvoted and clicked on downvote"
        else:
            query.is_active = True
            query.is_upvote = is_upvote_clicked
            message = "Made is_active True"
        query.save()
    except:
        query = UpvotesOnPosts(is_upvote=is_upvote_clicked, user=user, post=post)
        query.save()
        message = "Created new row"

    upvotes = UpvotesOnPosts.objects.filter(is_upvote=True, is_active=True, post=post).count()
    downvotes = UpvotesOnPosts.objects.filter(is_upvote=False, is_active=True, post=post).count()
    has_upvoted = UpvotesOnPosts.objects.filter(is_upvote=True, is_active=True, post=post, user=user).count()
    has_downvoted = UpvotesOnPosts.objects.filter(is_upvote=False, is_active=True, post=post, user=user).count()

    has_downvoted = getBooleanFromQueryCount(has_downvoted)
    has_upvoted = getBooleanFromQueryCount(has_upvoted)

    return JsonResponse({'message': message, 'upvotes': upvotes, 'downvotes': downvotes, 'has_upvoted': has_upvoted,
                         'has_downvoted': has_downvoted})


@csrf_exempt
def upvote_or_downvote_user(request):
    upvoter_id = request.POST.get('upvoter_id')
    user_id = request.POST.get('user_to_be_voted')
    is_upvote_clicked = request.POST.get('is_upvote_clicked')
    is_upvote_clicked = parseBoolean(is_upvote_clicked)

    upvoter = User.objects.get(pk=int(upvoter_id))
    user_voted = User.objects.get(pk=int(user_id))

    message = None

    try:
        query = UpvotesOnUsers.objects.get(user=user_voted, upvoter=upvoter)
        if query.is_active:
            if query.is_upvote and is_upvote_clicked:
                message = "Already upvoted and clicked on upvote"
            elif query.is_upvote and not is_upvote_clicked:
                query.is_active = False
                message = "Earlier upvoted but now no vote"
            elif not query.is_upvote and is_upvote_clicked:
                query.is_active = False
                message = "Earlier downvoted but now no vote"
            elif not query.is_upvote and not is_upvote_clicked:
                message = "Already downvoted and clicked on downvote"
        else:
            query.is_active = True
            query.is_upvote = is_upvote_clicked
            message = "Made is_active True"
        query.save()
    except:
        query = UpvotesOnUsers(is_upvote=is_upvote_clicked, user=user_voted, upvoter=upvoter)
        query.save()
        message = "Created new row"

    upvotes = UpvotesOnUsers.objects.filter(is_upvote=True, is_active=True, user=user_voted).count()
    downvotes = UpvotesOnUsers.objects.filter(is_upvote=False, is_active=True, user=user_voted).count()
    has_upvoted = UpvotesOnUsers.objects.filter(is_upvote=True, is_active=True, user=user_voted,
                                                upvoter=upvoter).count()
    has_downvoted = UpvotesOnUsers.objects.filter(is_upvote=False, is_active=True, user=user_voted,
                                                  upvoter=upvoter).count()

    has_downvoted = getBooleanFromQueryCount(has_downvoted)
    has_upvoted = getBooleanFromQueryCount(has_upvoted)

    return JsonResponse({'message': message, 'upvotes': upvotes, 'downvotes': downvotes, 'has_upvoted': has_upvoted,
                         'has_downvoted': has_downvoted})


@csrf_exempt
def get_people_who_saw_post(request):
    pagenumber = request.GET.get('pagenumber', 1)
    post_id = request.GET.get('post_id')

    post = Posts.objects.get(pk=int(post_id))

    query = PostSeens.objects.filter(post=post).order_by('-time')

    query_paginated = Paginator(query, 20)
    query = query_paginated.page(pagenumber)
    next_page = None
    if query.has_next():
        next_page = query.next_page_number()

    seens = []
    for saw in query:
        user_profile = saw.user.user_profile.get()
        seens.append(
            {'time': saw.time, 'image': user_profile.profile_image, 'name': user_profile.full_name, 'id': saw.user.id})

    return JsonResponse({'seens': seens, 'next_page': next_page})


@csrf_exempt
def get_students_posts(request):
    user_id = request.POST.get('user_id')
    user_id = int(user_id)
    pagenumber = request.GET.get('pagenumber', 1)

    user = User.objects.get(pk=user_id)
    user_profile = user.user_profile.get()

    teacher_posts = []
    query = Posts.objects.filter((Q(is_by_teacher=False))).order_by('-time')

    query_paginated = Paginator(query, 20)
    query = query_paginated.page(pagenumber)
    next_page = None
    if query.has_next():
        next_page = query.next_page_number()

    for post in query:
        temp = User.objects.get(pk=int(post.uploader.id)).user_profile.get()
        image = None
        try:
            image = post.image.url
        except:
            pass
        upvotes = UpvotesOnPosts.objects.filter(is_upvote=True, is_active=True, post=post).count()
        downvotes = UpvotesOnPosts.objects.filter(is_upvote=False, is_active=True, post=post).count()
        has_upvoted = UpvotesOnPosts.objects.filter(is_upvote=True, is_active=True, post=post, user=user).count()
        has_downvoted = UpvotesOnPosts.objects.filter(is_upvote=False, is_active=True, post=post, user=user).count()
        seens = PostSeens.objects.filter(post=post).count()
        saves = SavedPosts.objects.filter(post=post, is_active=True).count()
        is_saved = SavedPosts.objects.filter(post=post, user=user, is_active=True).count()
        category = post.category.name
        category_color = post.category.color

        has_downvoted = getBooleanFromQueryCount(has_downvoted)
        has_upvoted = getBooleanFromQueryCount(has_upvoted)
        is_saved = getBooleanFromQueryCount(is_saved)

        comment = CommentsOnPosts.objects.filter(post=post).count()

        teacher_posts.append(
            {'id': post.id, 'heading': post.heading, 'description': post.description, 'image': image, 'time': post.time,
             'user_image': temp.profile_image, 'user_name': temp.full_name, 'upvotes': upvotes, 'downvotes': downvotes,
             'has_upvoted': has_upvoted, 'has_downvoted': has_downvoted, 'comment': comment, 'seens': seens,
             'category': category, 'category_color': category_color, 'saves': saves, 'is_saved': is_saved,
             'user_id': post.uploader.id})

    return JsonResponse({'posts': teacher_posts, 'next_page': next_page})


@csrf_exempt
def post_detail_page(request):
    user_id = request.POST.get('user_id')
    post_id = request.POST.get('post_id')

    post = Posts.objects.get(pk=int(post_id))
    user = User.objects.get(pk=int(user_id))


def parseBoolean(stringToParse):
    if stringToParse == 'True' or stringToParse == "true" or stringToParse == 1 or stringToParse == True or stringToParse == 'TRUE':
        return True
    return False


@csrf_exempt
def user_profile_viewed_by_other(request):
    user_id = request.POST.get('user_id')
    id_find = request.POST.get('profile_viewing_id')

    user = User.objects.get(pk=int(user_id))
    user_profile = user.user_profile.get()

    query_user = User.objects.get(pk=int(id_find))
    query_user_profile = query_user.user_profile.get()

    branch = 'Not Available'
    batch = 'Not Available'
    year = 'Not Available'
    if query_user_profile.branch is not None:
        branch = query_user_profile.branch.branch_name
    if query_user_profile.batch is not None:
        batch = query_user_profile.batch.batch_name
    if query_user_profile.year is not None:
        year = str(query_user_profile.year.admission_year) + ' - ' + str(query_user_profile.year.passout_year)

    number_of_posts = Posts.objects.filter(uploader=query_user).count()

    email = None
    if query_user_profile.is_email_shown_to_others:
        email = query_user.email
    phone = None
    if query_user_profile.is_mobile_shown_to_others:
        phone = query_user_profile.mobile_number

    can_message = False
    if user_profile.is_student_coordinator or user_profile.is_professor or user_profile.is_senior_professor or query_user_profile.is_student_coordinator or query_user_profile.is_professor or query_user_profile.is_senior_professor:
        can_message = True

    upvotes = UpvotesOnUsers.objects.filter(is_upvote=True, is_active=True, user=query_user).count()
    downvotes = UpvotesOnUsers.objects.filter(is_upvote=False, is_active=True, user=query_user).count()
    has_upvoted = UpvotesOnUsers.objects.filter(is_upvote=True, is_active=True, user=query_user,
                                                upvoter=user).count()
    has_downvoted = UpvotesOnUsers.objects.filter(is_upvote=False, is_active=True, user=query_user,
                                                  upvoter=user).count()

    has_downvoted = getBooleanFromQueryCount(has_downvoted)
    has_upvoted = getBooleanFromQueryCount(has_upvoted)

    return JsonResponse({'name': query_user_profile.full_name, 'image': query_user_profile.profile_image,
                         'is_student_coordinator': query_user_profile.is_student_coordinator,
                         'designation': query_user_profile.designation, 'about': query_user_profile.about,
                         'branch': branch, 'batch': batch, 'year': year, 'number_of_posts': number_of_posts,
                         'resume': query_user_profile.resume, 'email': email, 'phone': phone,
                         'can_message': can_message, 'upvotes': upvotes, 'downvotes': downvotes,
                         'has_upvoted': has_upvoted, 'has_downvoted': has_downvoted,
                         'is_professor': query_user_profile.is_professor,
                         'is_senior_professor': query_user_profile.is_senior_professor})


@csrf_exempt
def get_all_post_categories(request):
    user_id = request.POST.get('user_id')

    user = User.objects.get(pk=int(user_id))
    user_profile = user.user_profile.get()

    message = None
    error = False

    if user_profile.has_reached_post_limit:
        message = 'You have been temporarily blocked from making posts. Please contact us using the contact us section to resolve that. Sorry for tthe inconvinience caused.'
        error = True
        return JsonResponse({'error': error, 'message': message})
    elif not user_profile.is_verified:
        message = 'Sorry but your profile details are pending verification from the our team. It may take a time of 1 working day. However, you can contact us from the contact us section if required about verification.'
        error = True
        return JsonResponse({'error': error, 'message': message})

    categories = []

    query = PostCategories.objects.filter(is_active=True)
    for cat in query:
        image = None
        try:
            image = cat.image.url
        except:
            pass
        categories.append({'id': cat.id, 'name': cat.name, 'image': image, 'type': cat.type, 'color': cat.color})

    return JsonResponse({'categories': categories, 'error': error, 'message': message})


@csrf_exempt
def get_all_teachers_list(request):
    pagenumber = request.GET.get('pagenumber', 1)
    user_id = request.POST.get('user_id')
    user = User.objects.get(pk=int(user_id))
    user_profile = user.user_profile.get()

    query = UserProfiles.objects.filter(college=user_profile.college).filter(
        Q(is_professor=True) | Q(is_senior_professor=True))

    query_paginated = Paginator(query, 20)
    query = query_paginated.page(pagenumber)
    next_page = None
    if query.has_next():
        next_page = query.next_page_number()

    teachers = []
    for teach in query:
        branch = None
        try:
            branch = teach.branch.branch_name
        except:
            pass
        teachers.append(
            {'id': teach.user_obj.id, 'name': teach.full_name, 'branch': branch, 'image': teach.profile_image})

    return JsonResponse({'teachers': teachers, 'next_page': next_page})


@csrf_exempt
def save_post_visibility(request):
    user_id = request.POST.get('user_id')
    user = User.objects.get(pk=int(user_id))
    name = request.POST.get('name')

    batches_array_request = request.POST.get('batches_id')
    batches_array = json.loads(batches_array_request)
    branches_array_request = request.POST.get('branches_id')
    branches_array = json.loads(branches_array_request)
    years_array_request = request.POST.get('years_id')
    years_array = json.loads(years_array_request)
    users_array_request = request.POST.get('teachers_id')
    user_array = json.loads(users_array_request)

    saved_post_visibility = SavedPostVisibilities(user=user, name=name)
    saved_post_visibility.save()

    for batch_id in batches_array:
        try:
            batch = Batches.objects.get(pk=int(batch_id))
            attribute = SavedPostVisibilitiesAttributes(batch=batch, visibility=saved_post_visibility,
                                                        type=SavedPostVisibilitiesAttributes.BATCH)
            attribute.save()
        except:
            pass

    for batch_id in branches_array:
        try:
            batch = Branches.objects.get(pk=int(batch_id))
            attribute = SavedPostVisibilitiesAttributes(branch=batch, visibility=saved_post_visibility,
                                                        type=SavedPostVisibilitiesAttributes.BRANCH)
            attribute.save()
        except:
            pass

    for batch_id in years_array:
        try:
            batch = StudentYears.objects.get(pk=int(batch_id))
            attribute = SavedPostVisibilitiesAttributes(year=batch, visibility=saved_post_visibility,
                                                        type=SavedPostVisibilitiesAttributes.YEAR)
            attribute.save()
        except:
            pass

    for batch_id in user_array:
        try:
            batch = User.objects.get(pk=int(batch_id))
            attribute = SavedPostVisibilitiesAttributes(teacher=batch, visibility=saved_post_visibility,
                                                        type=SavedPostVisibilitiesAttributes.TEACHER)
            attribute.save()
        except:
            pass

    return JsonResponse({'done': True})


@csrf_exempt
def get_saved_post_visibilities(request):
    user_id = request.POST.get('user_id')
    user = User.objects.get(pk=int(user_id))

    query = SavedPostVisibilities.objects.filter(user=user, is_active=True).order_by('-time')
    saves = []
    for save in query:
        saves.append({'id': save.id, 'name': save.name})

    return JsonResponse({'visibilities': saves})


@csrf_exempt
def get_posts_posted_by_user(request):
    user_id = request.POST.get('user_id')
    user_id = int(user_id)
    pagenumber = request.GET.get('pagenumber', 1)

    user = User.objects.get(pk=user_id)
    user_profile = user.user_profile.get()

    teacher_posts = []
    query = Posts.objects.filter(uploader=user).order_by('-time')

    query_paginated = Paginator(query, 20)
    query = query_paginated.page(pagenumber)
    next_page = None
    if query.has_next():
        next_page = query.next_page_number()

    for post in query:
        temp = User.objects.get(pk=int(post.uploader.id)).user_profile.get()
        image = None
        try:
            image = post.image.url
        except:
            pass
        upvotes = UpvotesOnPosts.objects.filter(is_upvote=True, is_active=True, post=post).count()
        downvotes = UpvotesOnPosts.objects.filter(is_upvote=False, is_active=True, post=post).count()
        has_upvoted = UpvotesOnPosts.objects.filter(is_upvote=True, is_active=True, post=post, user=user).count()
        has_downvoted = UpvotesOnPosts.objects.filter(is_upvote=False, is_active=True, post=post, user=user).count()
        seens = PostSeens.objects.filter(post=post).count()
        saves = SavedPosts.objects.filter(post=post, is_active=True).count()
        is_saved = SavedPosts.objects.filter(post=post, user=user, is_active=True).count()
        category = post.category.name
        category_color = post.category.color

        has_downvoted = getBooleanFromQueryCount(has_downvoted)
        has_upvoted = getBooleanFromQueryCount(has_upvoted)
        is_saved = getBooleanFromQueryCount(is_saved)

        comment = CommentsOnPosts.objects.filter(post=post).count()

        teacher_posts.append(
            {'id': post.id, 'heading': post.heading, 'description': post.description, 'image': image, 'time': post.time,
             'user_image': temp.profile_image, 'user_name': temp.full_name, 'upvotes': upvotes, 'downvotes': downvotes,
             'has_upvoted': has_upvoted, 'has_downvoted': has_downvoted, 'comment': comment, 'seens': seens,
             'category': category, 'category_color': category_color, 'saves': saves, 'is_saved': is_saved,
             'user_id': post.uploader.id})

    is_by_teacher = False
    if user_profile.is_senior_professor or user_profile.is_professor:
        is_by_teacher = True

    return JsonResponse({'posts': teacher_posts, 'next_page': next_page, 'is_by_teacher': is_by_teacher})


def getBooleanFromQueryCount(count):
    if count > 0:
        return True
    else:
        return False
