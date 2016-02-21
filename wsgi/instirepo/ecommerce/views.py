import base64
from ctypes import c_short
import datetime
from operator import itemgetter
import os

import sys
from django.core.files.base import ContentFile
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
from instirepo import settings
from ecommerce.models import *
from django.core import serializers
from push_notifications.models import GCMDevice
from django.db.models import Q, Count
import pdb

from instirepo_web.models import UserProfiles


@csrf_exempt
def get_all_categories_for_product(request):
    categories = []
    query = ProductCategories.objects.filter(is_active=True)
    for cat in query:
        image = None
        try:
            image = cat.image.url
        except:
            pass
        categories.append({'id': cat.id, 'name': cat.name, 'image': image})

    return JsonResponse({'categories': categories})


@csrf_exempt
def get_all_product_categories_and_trending_and_recent_products(request):
    user_id = request.GET.get('user_id')

    user = User.objects.get(pk=int(user_id))
    user_profile = user.user_profile.get()

    categories = []
    query = ProductCategories.objects.filter(is_active=True)
    for cat in query:
        image = None
        try:
            image = cat.image.url
        except:
            pass
        categories.append({'id': cat.id, 'name': cat.name, 'image': image})

    recently_viewed = []
    query = RecentlyViewedProducts.objects.filter(user=user).values('product', 'user').distinct()[:20]
    for pro in query:
        product = Product.objects.get(pk=int(pro['product']))
        image = None
        try:
            image = product.image1.url
        except:
            pass
        recently_viewed.append(
                {'id': product.id, 'name': product.name, 'mrp': product.mrp, 'price': product.price,
                 'image': image})

    trending_products = []
    time_delta_days_factor = 1
    yesterday = datetime.date.today() - datetime.timedelta(days=time_delta_days_factor)
    query = Product.objects.filter(recently_viewed__time__gt=yesterday, stock__gt=0, is_active=True,
                                   college=user_profile.college).annotate(
            views=Count('recently_viewed')).order_by('-views')[:20]

    while query.count() != 20:
        time_delta_days_factor += 1
        if time_delta_days_factor > 10:
            break
        yesterday = datetime.date.today() - datetime.timedelta(days=time_delta_days_factor)
        query = Product.objects.filter(recently_viewed__time__gt=yesterday, stock__gt=0, is_active=True,
                                       college=user_profile.college).annotate(
                views=Count('recently_viewed')).order_by('-views')[:20]

    for pro in query:
        image = None
        try:
            image = pro.image1.url
        except:
            pass
        trending_products.append({'id': pro.id, 'name': pro.name, 'mrp': pro.mrp, 'price': pro.price,
                                  'image': image, 'views': pro.views})

    return JsonResponse(
            {'categories': categories, 'recently_viewed': recently_viewed, 'trending_products': trending_products})


@csrf_exempt
def get_products_from_category(request):
    user_id = request.GET.get('user_id')
    category_id = request.GET.get('category_id')
    page_number = request.GET.get('page_number', 1)
    page_size = request.GET.get('page_size', 20)

    user = User.objects.get(pk=int(user_id))
    user_profile = user.user_profile.get()
    category = ProductCategories.objects.get(pk=int(category_id))

    query = Product.objects.filter(stock__gt=0, is_active=True, category=category, college=user_profile.college)

    query_paginated = Paginator(query, page_size)
    query = query_paginated.page(page_number)
    next_page = None
    if query.has_next():
        next_page = query.next_page_number()

    products = []
    for pro in query:
        image = None
        try:
            image = pro.image1.url
        except:
            pass
        products.append({'id': pro.id, 'name': pro.name, 'mrp': pro.mrp, 'price': pro.price,
                         'image': image})

    return JsonResponse({'products': products, 'next_page': next_page})


@csrf_exempt
def get_trending_products(request):
    user_id = request.GET.get('user_id')
    page_number = request.GET.get('page_number', 1)
    page_size = request.GET.get('page_size', 20)

    user = User.objects.get(pk=int(user_id))
    user_profile = user.user_profile.get()

    time_delta_days_factor = 1
    yesterday = datetime.date.today() - datetime.timedelta(days=time_delta_days_factor)
    query = Product.objects.filter(recently_viewed__time__gt=yesterday, stock__gt=0, is_active=True,
                                   college=user_profile.college).annotate(views=Count('recently_viewed')).order_by(
            '-views')

    while query.count() < 40:
        time_delta_days_factor += 1
        if time_delta_days_factor > 10:
            break
        yesterday = datetime.date.today() - datetime.timedelta(days=time_delta_days_factor)
        query = Product.objects.filter(recently_viewed__time__gt=yesterday, stock__gt=0, is_active=True,
                                       college=user_profile.college).annotate(views=Count('recently_viewed')).order_by(
                '-views')

    query_paginated = Paginator(query, page_size)
    query = query_paginated.page(page_number)
    next_page = None
    if query.has_next():
        next_page = query.next_page_number()

    products = []
    for pro in query:
        image = None
        try:
            image = pro.image1.url
        except:
            pass
        products.append({'id': pro.id, 'name': pro.name, 'mrp': pro.mrp, 'price': pro.price,
                         'image': image})

    return JsonResponse({'products': products, 'next_page': next_page})


@csrf_exempt
def get_recent_products(request):
    user_id = request.GET.get('user_id')
    page_number = request.GET.get('page_number', 1)
    page_size = request.GET.get('page_size', 20)

    user = User.objects.get(pk=int(user_id))
    user_profile = user.user_profile.get()

    recently_viewed = []
    query = RecentlyViewedProducts.objects.filter(user=user).values('product', 'user').distinct()

    query_paginated = Paginator(query, page_size)
    query = query_paginated.page(page_number)
    next_page = None
    if query.has_next():
        next_page = query.next_page_number()

    for pro in query:
        product = Product.objects.get(pk=int(pro['product']))
        image = None
        try:
            image = product.image1.url
        except:
            pass
        recently_viewed.append(
                {'id': product.id, 'name': product.name, 'mrp': product.mrp, 'price': product.price,
                 'image': image})

    return JsonResponse({'products': recently_viewed, 'next_page': next_page})


@csrf_exempt
def get_product_detail(request):
    user_id = request.GET.get('user_id')
    product_id = request.GET.get('product_id')

    user = User.objects.get(pk=int(user_id))
    user_profile = user.user_profile.get()

    product = Product.objects.get(pk=int(product_id))

    image1 = None
    image2 = None
    image3 = None
    image4 = None
    image5 = None
    image6 = None
    image7 = None
    image8 = None
    try:
        image1 = product.image1.url
    except:
        pass
    try:
        image2 = product.image2.url
    except:
        pass
    try:
        image3 = product.image3.url
    except:
        pass
    try:
        image4 = product.image4.url
    except:
        pass
    try:
        image5 = product.image5.url
    except:
        pass
    try:
        image6 = product.image6.url
    except:
        pass
    try:
        image7 = product.image7.url
    except:
        pass
    try:
        image8 = product.image8.url
    except:
        pass

    uploader = product.uploader.user_profile.get()

    number_of_comments = ProductComments.objects.filter(product=product, is_active=True).count()
    number_of_likes = ProductFavourites.objects.filter(product=product, is_active=True).count()
    has_liked = ProductFavourites.objects.filter(product=product, is_active=True, user=user).count()
    has_liked = getBooleanFromQueryCount(has_liked)

    recent_add = RecentlyViewedProducts(user=user, product=product, time=datetime.datetime.now())
    recent_add.save()

    return JsonResponse(
            {'name': product.name, 'id': product.id, 'mrp': product.mrp, 'price': product.price, 'image': image1,
             'image2': image2, 'image3': image3, 'image4': image4, 'image5': image5, 'image6': image6, 'image7': image7,
             'image8': image8, 'stock': product.stock, 'description': product.description,
             'contact_number': product.contact_number, 'user_name': uploader.full_name, 'user_id': product.uploader.id,
             'user_image': uploader.profile_image, 'time': product.time, 'bill_availabe': product.bill_availabe,
             'warranty_left': product.warranty_left, 'number_of_comments': number_of_comments,
             'number_of_likes': number_of_likes, 'has_liked': has_liked,
             'warranty_availabe': product.warranty_availabe})


@csrf_exempt
def get_comments_on_product(request):
    pagenumber = request.GET.get('pagenumber', 1)
    user_id = request.POST.get('user_id')
    product_id = request.GET.get('product_id')

    product = Product.objects.get(pk=int(product_id))

    query = ProductComments.objects.filter(product=product, is_active=True).order_by('-time')
    count = ProductComments.objects.filter(product=product, is_active=True).count()

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
        is_flagged = False
        is_flag_query = CommentsFlags.objects.filter(is_active=True, user__id=int(user_id), comment=comment).count()
        if is_flag_query > 0:
            is_flagged = True
        comments.append({'id': comment.id, 'comment': comment.comment, 'time': comment.time, 'user_name': user_name,
                         'user_image': user_image, 'is_by_user': is_by_user, 'is_different_color': is_different_color,
                         'is_flagged': is_flagged, 'user_id': comment.user.id})

    return JsonResponse({'comments': comments, 'next_page': next_page, 'count': count})


@csrf_exempt
def add_comment_on_product(request):
    user_id = request.POST.get('user_id')
    product_id = request.POST.get('product_id')
    comment = request.POST.get('comment')

    user = User.objects.get(pk=int(user_id))
    product = Product.objects.get(pk=int(product_id))
    user_profile = user.user_profile.get()

    query = ProductComments(comment=comment, user=user, product=product)
    query.save()

    count = ProductComments.objects.filter(product=product, is_active=True).count()

    return JsonResponse(
            {'count': count, 'id': query.id, 'name': user_profile.full_name, 'image': user_profile.profile_image})


@csrf_exempt
def flag_comment_on_product(request):
    user_id = request.POST.get('user_id')
    user_id = int(user_id)
    comment_id = request.POST.get('comment_id')
    comment_id = int(comment_id)

    user = User.objects.get(pk=user_id)
    comment = ProductComments.objects.get(pk=comment_id)

    is_flagged = True
    try:
        query = CommentsFlags.objects.get(user=user, comment=comment)
        if query.is_active:
            query.is_active = False
            is_flagged = False
        else:
            query.is_active = True
        query.save()
    except:
        query = CommentsFlags(user=user, comment=comment)
        query.save()

    return JsonResponse({'is_flagged': is_flagged})


@csrf_exempt
def save_product_for_later(request):
    user_id = request.POST.get('user_id')
    product_id = request.POST.get('product_id')

    product = Product.objects.get(pk=int(product_id))
    user = User.objects.get(pk=int(user_id))

    is_saved = True
    try:
        query = ProductFavourites.objects.get(product=product, user=user)
        if query.is_active:
            query.is_active = False
            is_saved = False
        else:
            query.is_active = True
        query.save()
    except:
        query = ProductFavourites(product=product, user=user)
        query.save()

    count = ProductFavourites.objects.filter(product=product, is_active=True).count()

    return JsonResponse({'count': count, 'is_saved': is_saved})


@csrf_exempt
def upload_product(request):
    name = request.POST.get('name')
    description = request.POST.get('description')
    image1 = request.POST.get('image1')
    image2 = request.POST.get('image2')
    image3 = request.POST.get('image3')
    image4 = request.POST.get('image4')
    image5 = request.POST.get('image5')
    image6 = request.POST.get('image6')
    image7 = request.POST.get('image7')
    image8 = request.POST.get('image8')
    mrp = request.POST.get('mrp')
    price = request.POST.get('price')
    contact = request.POST.get('contact')
    warranty_left = request.POST.get('warranty_left')
    is_warranty = request.POST.get('is_warranty')
    is_bill = request.POST.get('is_bill')
    user_id = request.POST.get('user_id')
    category_id = request.POST.get('category_id')

    user = User.objects.get(pk=int(user_id))
    category = ProductCategories.objects.get(pk=int(category_id))

    product = Product(name=name, description=description, mrp=mrp, price=price, category=category,
                      contact_number=contact, bill_availabe=is_bill, warranty_availabe=is_warranty,
                      warranty_left=warranty_left, uploader=user, college=user.user_profile.get().college)

    if image1 is not None:
        data = base64.b64decode(image1)
        filename = "uploaded_image%s.png" % str(datetime.datetime.now()).replace('.', '_')
        product.image1 = ContentFile(data, filename)

    if image2 is not None:
        data = base64.b64decode(image2)
        filename = "uploaded_image%s.png" % str(datetime.datetime.now()).replace('.', '_')
        product.image2 = ContentFile(data, filename)
    if image3 is not None:
        data = base64.b64decode(image3)
        filename = "uploaded_image%s.png" % str(datetime.datetime.now()).replace('.', '_')
        product.image3 = ContentFile(data, filename)
    if image4 is not None:
        data = base64.b64decode(image4)
        filename = "uploaded_image%s.png" % str(datetime.datetime.now()).replace('.', '_')
        product.image4 = ContentFile(data, filename)
    if image5 is not None:
        data = base64.b64decode(image5)
        filename = "uploaded_image%s.png" % str(datetime.datetime.now()).replace('.', '_')
        product.image5 = ContentFile(data, filename)
    if image6 is not None:
        data = base64.b64decode(image6)
        filename = "uploaded_image%s.png" % str(datetime.datetime.now()).replace('.', '_')
        product.image6 = ContentFile(data, filename)
    if image7 is not None:
        data = base64.b64decode(image7)
        filename = "uploaded_image%s.png" % str(datetime.datetime.now()).replace('.', '_')
        product.image7 = ContentFile(data, filename)
    if image8 is not None:
        data = base64.b64decode(image8)
        filename = "uploaded_image%s.png" % str(datetime.datetime.now()).replace('.', '_')
        product.image8 = ContentFile(data, filename)

    product.save()

    return JsonResponse({'status': True})


def getBooleanFromQueryCount(count):
    if count > 0:
        return True
    else:
        return False
