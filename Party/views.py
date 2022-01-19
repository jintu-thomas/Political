from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
from str2bool import str2bool
from .models import Party_Name
import ast
from django.http import JsonResponse
from django.core.paginator import Paginator

# Create your views here.

@csrf_exempt
def adding_party_name(request):
    status = ''
    message = ''
    status_code = ''

    try:
        requestData = json.loads(request.body)
    except:
        requestData = request.POST

    try:
        party_name = requestData.get(u"party_name", None)
        added_date = datetime.now()
        party_image = None

        if "party_image" in request.FILES:
            party_image = request.FILES['party_image']

        #[{"name":"Party","status":"true"}]
        party_name = ast.literal_eval(str(party_name))

        try:
            for i in party_name:
                Party_Name.objects.get_or_create(party_name=(i['name']),\
                                                 defaults={'status': str2bool(i['status']), 'party_image': party_image,\
                                                           'added_datetime': added_date})
                status = "Success"
                message = "Successfully party_name was created"
                status_code = 200

        except Exception as e:
            status = "Failed"
            message = str(e)
            status_code = 409

    except Exception as e:
        status = "Failed"
        message = str(e)
        status_code = 409
    return JsonResponse({"status": status, "message": message, "status_code": status_code})

###getting_party_names:
@csrf_exempt
def getting_party_names(request):
    status = ''
    message = ''
    status_code = ''
    total_page = ''
    index_page = ''
    json_data = []
    data = dict()

    try:
        requestData = json.loads(request.body)
    except:
        requestData = request.POST
    try:
        page = requestData.get(u"page", None)
        total_parties = Party_Name.objects.all()

        if total_parties.exists():
            parties_paginator = Paginator(total_parties, 10)
            if int(page) > 0:
                pag_num = parties_paginator.get_page(page)
                n_parties_pg = str(pag_num)[1:-1]
                n = [int(i) for i in n_parties_pg.split() if i.isdigit()]
                total_page = str(n[1])

                if int(page) <= int(total_page):
                    for obj in pag_num:
                        data1 = {"primary_key": obj.primary_key, "party_name": obj.party_name,\
                                 "party_image": str(obj.party_image), "status": obj.status,\
                                 "added_datetime": obj.added_datetime, "updated_datetime": obj.updated_datetime}
                        json_data.append(data1)

                    index_page = str(n[0])
                    status = "Success"
                    message = "Successfully received the parties"
                    status_code = 200

                else:
                    status = "Failed"
                    message = "Total party_names pages across the limit"
                    status_code = 409
            else:
                status = "Failed"
                message = "Total party_names pages beyond the limit"
                status_code = 409

    except Exception as e:
        status = "Failed"
        message = str(e)
        status_code = 407

    return JsonResponse({"status": status, "data": json_data, "message": message,
                         "status_code": status_code, "total_page": total_page, "index_page": index_page})

###Updating_Party_name:
@csrf_exempt
def updating_party_names(request):
    status = ''
    message = ''
    status_code = ''
    try:
        requestData = json.loads(request.body)
    except:
        requestData = request.POST

    try:
        primary_key = requestData.get(u"primary_key", None)
        new_party_name = requestData.get(u"new_party_name", None)
        new_status = requestData.get(u"new_status", None)
        updated_datetime = datetime.now()
        new_party_image = None

        if "new_party_image" in request.FILES:
            new_party_image = request.FILES['new_party_image']

        try:
            get_party_names = Party_Name.objects.get(primary_key=primary_key)

            if new_party_name != None and new_party_name != "":
                check_party_name = Party_Name.objects.filter(party_name__iexact=new_party_name)
                if check_party_name.exists() == False:
                    get_party_names.party_name = new_party_name
                    get_party_names.party_image = new_party_image
                    get_party_names.party_status = str2bool(new_status)
                    get_party_names.updated_datetime = updated_datetime
                    get_party_names.save()

                    status = "Success"
                    message = "Party_Names was successfully updated"
                    status_code = 200

                else:
                    status = "Failed"
                    message = "Party_names already exists"
                    status_code = 407
            else:
                status = "Failed"
                message = "Party_names cannot be empty"
                status_code = 407

        except Exception as e:
            status = "Failed"
            message = str(e)
            status_code = 409

    except Exception as e:
        status = "Failed"
        message = str(e)
        status_code = 409
    return JsonResponse({"status": status, "message": message, "status_code": status_code})
