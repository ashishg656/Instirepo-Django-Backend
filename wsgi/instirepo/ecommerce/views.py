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

    return JsonResponse(
            {'name': product.name, 'id': product.id, 'mrp': product.mrp, 'price': product.price, 'image': image1,
             'image2': image2, 'image3': image3, 'image4': image4, 'image5': image5, 'image6': image6, 'image7': image7,
             'image8': image8, 'stock': product.stock, 'description': product.description,
             'contact_number': product.contact_number, 'user_name': uploader.full_name, 'user_id': product.uploader.id,
             'user_image': uploader.profile_image, 'time': product.time, 'bill_availabe': product.bill_availabe,
             'warranty_left': product.warranty_left, 'number_of_comments': number_of_comments,
             'number_of_likes': number_of_likes, 'has_liked': has_liked})


def getBooleanFromQueryCount(count):
    if count > 0:
        return True
    else:
        return False
