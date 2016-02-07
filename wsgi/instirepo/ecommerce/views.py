import base64
from ctypes import c_short
from datetime import datetime, time
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
from django.db.models import Q
import pdb


@csrf_exempt
def get_all_product_categories_and_trending_and_recent_products(request):
    user_id = request.POST.get('user_id')

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
    query = RecentlyViewedProducts.objects.filter(user=user).order_by(
            '-time').values('product', 'user').distinct()
    for pro in query:
        pro = pro['product']
        image = None
        try:
            image = pro.product.image1.url
        except:
            pass
        recently_viewed.append(
                {'id': pro.product.id, 'name': pro.product.name, 'mrp': pro.product.mrp, 'price': pro.product.price,
                 'image': image})

    return JsonResponse({'categories': categories,'recently_viewed':recently_viewed})
