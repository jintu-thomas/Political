from re import I
from django.shortcuts import render


from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
from str2bool import str2bool
from .models import State_Name,Assembly_Name
import ast
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Mandal_Name

# Create your views here.

@csrf_exempt
def adding_mandal_name(request):
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
        added_date = datetime.now()

        # [{"name":"Chennai","status":"true"}]
        mandal_name = ast.literal_eval(str(mandal_name))

        try:
            states = State_Name.objects.get(primary_key=state_name)
            get_assembly = Assembly_Name.objects.get(primary_key=assembly_name, state_name=states)
            for i in mandal_name:
                Mandal_Name.objects.get_or_create(state_name=states, assembly_name=get_assembly,\
                                                  mandal_name=(i['name']),\
                                                  defaults={'status': str2bool(i['status']), 'added_datetime': added_date})
                status = "Success"
                message = "Successfully mandal_name was created"
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


###Getting_Mandals_Names:
@csrf_exempt
def getting_mandal_names(request):
    status = ''
    message = ''
    status_code = ''
    total_page = ''
    index_page = ''
    json_data = []
    data = dict()

    try:
        requestData = json.loads(request)
    except:
        requestData = request.POST

    try:
        page = requestData.get(u"page", None)
        state_name = requestData.get(u"state_name", None)
        assembly_name = requestData.get(u"assembly_name", None)

        states = State_Name.objects.get(primary_key=state_name)
        get_assembly = Assembly_Name.objects.get(primary_key=assembly_name, state_name=states)
        total_mandals = Mandal_Name.objects.filter(state_name=states, assembly_name=get_assembly)

        if total_mandals.exists():
            mandal_paginator = Paginator(total_mandals, 10)
            if int(page) > 0:
                pag_num = mandal_paginator.get_page(page)
                n_mandalpg = str(pag_num)[1:-1]
                n = [int(i) for i in n_mandalpg.split() if i.isdigit()]
                total_page = str(n[1])

                if int(page) <= int(total_page):
                    for obj in pag_num:
                        data1 = {"primary_key": obj.primary_key, "mandal_name": obj.mandal_name,\
                                 "status": obj.status, "added_datetime": obj.added_datetime, "updated_datetime": obj.updated_datetime}
                        json_data.append(data1)

                    index_page = str(n[0])
                    status = "Success"
                    message = "Successfully received the mandals"
                    status_code = 200

                else:
                    status = "Failed"
                    message = "Total mandal_name pages across the limit"
                    status_code = 407
            else:
                status = "Failed"
                message = "Total mandal_name pages beyond the limit"
                status_code = 407

    except Exception as e:
        status = "Failed"
        message = str(e)
        status_code = 409
    return JsonResponse({"status": status, "data": json_data, "message": message,
                         "status_code": status_code, "total_page": total_page, "index_page": index_page})

###Updating_Mandal_Names:
@csrf_exempt
def updating_mandal_names(request):
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
        assembly_name = requestData.get(u"assembly_name", None)
        new_mandal_name = requestData.get(u"new_mandal_name", None)
        new_status = requestData.get(u"new_status", None)
        updated_datetime = datetime.now()

        states = State_Name.objects.get(primary_key=state_name)
        get_assembly = Assembly_Name.objects.get(primary_key=assembly_name, state_name=states)
        get_mandal = Mandal_Name.objects.get(primary_key=primary_key, state_name=states, assembly_name=get_assembly)

        if new_mandal_name !=None and new_mandal_name != "":
            check_mandal_names = Mandal_Name.objects.filter(mandal_name__iexact=new_mandal_name)
            if check_mandal_names.exists() == False:
                get_mandal.mandal_name = new_mandal_name
                get_mandal.status = str2bool(new_status)
                get_mandal.updated_datetime = updated_datetime
                get_mandal.save()

                status = "Success"
                message = "Successfully updated the mandal_name"
                status_code = "200"

            else:
                status = "Failed"
                message = "Mandal_Name already exists"
                status_code = 407
        else:
            status = "Failed"
            message = "Mandal_Name cannot be empty"
            status_code = 407

    except Exception as e:
        status = "Failed"
        message = str(e)
        status_code = 409
    return JsonResponse({"status": status, "message": message, "status_code": status_code})
