from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
from str2bool import str2bool
from .models import State_Name,Assembly_Name
import ast
from django.http import JsonResponse
from django.core.paginator import Paginator
from Mandal.models import Mandal_Name
from .models import Village_Name
# Create your tests here.

@csrf_exempt
def adding_village_name(request):
    status = ''
    message = ''
    status_code = ''

    try:
        requestData = json.loads(request.body)
    except:
        requestData = request.POST

    try:
        state_name = requestData.get(u"state_name", None)
        assembly_name = requestData.get(u"assembly_name", None)
        mandal_name = requestData.get(u"mandal_name", None)
        village_name = requestData.get(u"village_name", None)
        added_date = datetime.now()

        # [{"name":"Chennai South","status":"true"}]
        village_name = ast.literal_eval(str(village_name))

        try:
            states = State_Name.objects.get(primary_key=state_name)
            get_assembly = Assembly_Name.objects.get(primary_key=assembly_name, state_name=states)
            get_mandal_name = Mandal_Name.objects.get(primary_key=mandal_name, state_name=states, assembly_name=get_assembly)

            for i in village_name:
                Village_Name.objects.get_or_create(state_name=states, assembly_name=get_assembly, mandal_name=get_mandal_name,\
                                                   village_name=(i['name']),\
                                                   defaults={'status': str2bool(i['status']), 'added_datetime': added_date})
                status = "Success"
                message = "Successfully village_name was created"
                status_code = 200

        except Exception as e:
            status = "Failed"
            message = str(e)
            status_code = 407

    except Exception as e:
        status = "Failed"
        message = str(e)
        status_code = 407
    return JsonResponse({"status": status, "message": message, "status_code": status_code})

###Getting_Village_Names:
@csrf_exempt
def getting_village_names(request):
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
        state_name = requestData.get(u"state_name", None)
        assembly_name = requestData.get(u"assembly_name", None)
        mandal_name = requestData.get(u"mandal_name", None)

        states = State_Name.objects.get(primary_key=state_name)
        get_assembly = Assembly_Name.objects.get(primary_key=assembly_name, state_name=states)
        get_mandal_name = Mandal_Name.objects.get(primary_key=mandal_name, state_name=states, assembly_name=get_assembly)
        total_villages = Village_Name.objects.filter(state_name=states, assembly_name=get_assembly, mandal_name=get_mandal_name)

        if total_villages.exists():
            village_paginator = Paginator(total_villages, 10)
            if int(page) > 0:
                pag_num = village_paginator.get_page(page)
                n_villagepg = str(pag_num)[1:-1]
                n = [int(i) for i in n_villagepg.split() if i.isdigit()]
                total_page = str(n[1])

                if int(page) <= int(total_page):
                    for obj in pag_num:
                        data1 = {"primary_key": obj.primary_key, "village_name": obj.village_name, "status": obj.status,\
                                 "added_datetime": obj.added_datetime, "updated_datetime": obj.updated_datetime}
                        json_data.append(data1)

                    index_page = str(n[0])
                    status = "Success"
                    message = "Successfully received the villages"
                    status_code = 200

                else:
                    status = "Failed"
                    message = "Total village_name pages across the limit"
                    status_code = 407
            else:
                status = "Failed"
                message = "Total village_name pages beyond the limit"
                status_code = 407
                
    except Exception as e:
        status = "Failed"
        message = str(e)
        status_code = 409
    return JsonResponse({"status": status, "data": json_data, "message": message,
                         "status_code": status_code, "total_page": total_page, "index_page": index_page})

#Updating_Village_Names:
@csrf_exempt
def updating_village_names(request):
    status = ''
    message = ''
    status_code = ''

    try:
        requestData = json.loads(request.body)
    except:
        requestData = request.POST

    try:
        primary_key = requestData.get(u"primary_key", None)
        state_name = requestData.get(u"state_name", None)
        assembly_name  = requestData.get(u"assembly_name", None)
        mandal_name = requestData.get(u"mandal_name", None)
        new_village_name = requestData.get(u"new_village_name", None)
        new_status = requestData.get(u"new_status", None)
        updated_datetime = datetime.now()

        states = State_Name.objects.get(primary_key=state_name)
        get_assembly = Assembly_Name.objects.get(primary_key=assembly_name, state_name=states)
        get_mandal_name = Mandal_Name.objects.get(primary_key=mandal_name, state_name=states, assembly_name=get_assembly)
        get_village = Village_Name.objects.get(primary_key=primary_key, state_name=states, assembly_name=get_assembly, mandal_name=get_mandal_name)

        if new_village_name !=None and new_village_name != "":
            check_village_names = Village_Name.objects.filter(village_name__iexact=new_village_name)
            if check_village_names.exists() == False:
                get_village.village_name = new_village_name
                get_village.status = str2bool(new_status)
                get_village.updated_datetime = updated_datetime
                get_village.save()

                status = "Success"
                message = "Successfully updated the village_name"
                status_code = "200"

            else:
                status = "Failed"
                message = "Village_Name already exists"
                status_code = 407
        else:
            status = "Failed"
            message = "Village_Name cannot be empty"
            status_code = 407

    except Exception as e:
        status = "Failed"
        message = str(e)
        status_code = 409
    return JsonResponse({"status": status, "message": message, "status_code": status_code})
