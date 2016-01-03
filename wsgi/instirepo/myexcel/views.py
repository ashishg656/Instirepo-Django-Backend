import base64
from ctypes import c_short
from datetime import datetime, time
from operator import itemgetter
import os
from myexcel.models import *
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
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from instirepo import settings
from instirepo_web.models import *
from django.core import serializers
from push_notifications.models import GCMDevice
from django.db.models import Q


@csrf_exempt
def get_works_list(request):
    pagenumber = request.GET.get('pagenumber', 1)

    query = Works.objects.all()

    query_paginated = Paginator(query, 20)
    query = query_paginated.page(pagenumber)
    next_page = None
    if query.has_next():
        next_page = query.next_page_number()

    works = []
    for work in query:
        works.append(
            {'id': work.id, 'toolNumber': work.tool_number, 'jwNumber': work.jw_number, 'date': work.date,
             'product': work.product, 'description': work.description, 'startDate': work.start_date,
             'targetDate': work.target_date, 'doneBy': work.done_by,
             'actualDateOfCompletion': work.actual_date, 'remarks': work.remarks, 'cost': work.cost,
             'status': work.status})

    return JsonResponse({'works': works, 'next_page': next_page})


@csrf_exempt
def add_work(request):
    tool_number = request.POST.get('tool_number')
    jw_number = request.POST.get('jw_number')
    product = request.POST.get('product')
    desc = request.POST.get('desc')
    startdate = request.POST.get('startdate')
    targetdate = request.POST.get('targetdate')
    doneby = request.POST.get('doneby')
    actualdate = request.POST.get('actualdate')
    cost = request.POST.get('cost')
    status = request.POST.get('status')
    remarks = request.POST.get('remarks')
    id_work = request.POST.get('id_work')

    work = None
    if id_work is None:
        work = Works()
        work.tool_number = tool_number
        work.jw_number = jw_number
        work.product = product
        work.description = desc
        work.start_date = startdate
        work.target_date = targetdate
        work.done_by = doneby
        work.actual_date = actualdate
        work.cost = cost
        work.status = status
        work.remarks = remarks
        work.save()
    else:
        pass

    return JsonResponse({'id': work.id})
