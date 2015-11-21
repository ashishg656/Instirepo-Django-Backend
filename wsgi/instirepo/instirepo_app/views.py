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
    college = College.objects.get(pk=int(college_id))

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
             'category': category, 'category_color': category_color, 'saves': saves, 'is_saved': is_saved})

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
    post_id = request.POST.get('post_id')

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
        comments.append({'id': comment.id, 'comment': comment.comment, 'time': comment.time, 'user_name': user_name,
                         'user_image': user_image, 'is_by_user': is_by_user})

    return JsonResponse({'comments': comments, 'next_page': next_page, 'count': count})


@csrf_exempt
def add_comment_on_post(request):
    user_id = request.POST.get('user_id')
    post_id = request.POST.get('post_id')
    comment = request.POST.get('comment')

    user = User.objects.get(pk=int(user_id))
    post = Posts.objects.get(pk=int(post_id))

    query = CommentsOnPosts(comment=comment, user=user, post=post)
    query.save()

    count = CommentsOnPosts.objects.filter(post=post, is_active=True).count()

    return JsonResponse({'count': count, 'id': query.id})


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

    return JsonResponse({'message': message, 'upvotes': upvotes, 'downvotes': downvotes, 'has_upvoted': has_upvoted,
                         'has_downvoted': has_downvoted})


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
        if has_upvoted > 0:
            has_upvoted = True
            has_downvoted = False
        elif has_downvoted > 0:
            has_upvoted = False
            has_downvoted = False
        else:
            has_downvoted = False
            has_upvoted = False
        comment = CommentsOnPosts.objects.filter(post=post).count()

        teacher_posts.append(
            {'id': post.id, 'heading': post.heading, 'description': post.description, 'image': image, 'time': post.time,
             'user_image': temp.profile_image, 'user_name': temp.full_name, 'upvotes': upvotes, 'downvotes': downvotes,
             'has_upvoted': has_upvoted, 'has_downvoted': has_downvoted, 'comment': comment})

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


def getBooleanFromQueryCount(count):
    if count > 0:
        return True
    else:
        return False
