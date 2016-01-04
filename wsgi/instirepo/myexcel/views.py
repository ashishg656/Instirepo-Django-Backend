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

    query = Works.objects.filter(is_active=True).order_by('-date')

    query_paginated = Paginator(query, 30)
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
        work = Works.objects.get(pk=int(id_work))
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

    return JsonResponse({'id': work.id})


@csrf_exempt
def delete_work(request):
    id_work = request.POST.get('id_work')

    work = Works.objects.get(pk=int(id_work))
    work.is_active = False
    work.save()

    return JsonResponse({'status': True})


@csrf_exempt
def add_detail(request):
    work_id = request.POST.get('work_id')
    expected_date = request.POST.get('expected_date')
    actual_date = request.POST.get('actual_date')
    trial_date = request.POST.get('trial_date')
    qc_date = request.POST.get('qc_date')
    action_taken = request.POST.get('action_taken')
    status = request.POST.get('status')
    cost = request.POST.get('cost')
    remarks = request.POST.get('remarks')

    query = Details()
    query.work = Works.objects.get(pk=int(work_id))
    query.expected_date = expected_date
    query.actual_date = actual_date
    query.trial_date = trial_date
    query.qc_date = qc_date
    query.action_taken = action_taken
    query.status = status
    query.cost = cost
    query.remarks = remarks
    query.save()

    return JsonResponse({'id': query.id})


@csrf_exempt
def get_details_list(request):
    pagenumber = request.GET.get('pagenumber', 1)
    work_id = request.POST.get('work_id')
    work = Works.objects.get(pk=int(work_id))

    query = Details.objects.filter(is_active=True, work=work).order_by('-date')

    query_paginated = Paginator(query, 30)
    query = query_paginated.page(pagenumber)
    next_page = None
    if query.has_next():
        next_page = query.next_page_number()

    works = []
    for work in query:
        works.append(
            {'id': work.id, 'date': work.date, 'expectedDate': work.expected_date, 'actualDate': work.actual_date,
             'trialDate': work.trial_date, 'qcDate': work.qc_date, 'actionTaken': work.action_taken,
             'status': work.status, 'cost': work.cost,
             'remarks': work.remarks})

    return JsonResponse({'works': works, 'next_page': next_page})
