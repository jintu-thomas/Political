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
from Village.models import Village_Name
from .models import Booth_Name


# Create your views here.

@csrf_exempt
def adding_booth_name(request):
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
        booth_name = requestData.get(u"booth_name", None)
        added_date = datetime.now()

        # [{"name":"Kerala Booth","status":"true"}]
        booth_name = ast.literal_eval(str(booth_name))
        try:
            states = State_Name.objects.get(primary_key=state_name)
            get_assembly = Assembly_Name.objects.get(primary_key=assembly_name, state_name=states)
            get_mandal_name = Mandal_Name.objects.get(primary_key=mandal_name, state_name=states, assembly_name=get_assembly)
            get_village_name = Village_Name.objects.get(primary_key=village_name, state_name=states, assembly_name=get_assembly, mandal_name=get_mandal_name)

            for i in booth_name:
                Booth_Name.objects.get_or_create(state_name=states, assembly_name=get_assembly, mandal_name=get_mandal_name, village_name=get_village_name,\
                                                 booth_name=(i['name']),\
                                                 defaults={'status': str2bool(i['status']), 'added_datetime': added_date})
                status = "Success"
                message = "Successfully Booth_Name was created"
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

###Getting_Booth_Names:
@csrf_exempt
def getting_booth_names(request):
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
        mandal_name = requestData.get(u"mandal_name", None)
        village_name = requestData.get(u"village_name", None)

        states = State_Name.objects.get(primary_key=state_name)
        get_assembly = Assembly_Name.objects.get(primary_key=assembly_name, state_name=states)
        get_mandal_name = Mandal_Name.objects.get(primary_key=mandal_name, state_name=states, assembly_name=get_assembly)
        get_village_name = Village_Name.objects.get(primary_key=village_name, state_name=states, assembly_name=get_assembly,\
                                                        mandal_name=get_mandal_name)
        total_booths = Booth_Name.objects.filter(state_name=states, assembly_name=get_assembly,\
                                                     mandal_name=get_mandal_name, village_name=get_village_name)

        if total_booths.exists():
            booth_paginator = Paginator(total_booths, 10)
            if int(page) > 0:
                pag_num = booth_paginator.get_page(page)
                n_boothpg = str(pag_num)[1:-1]
                n = [int(i) for i in n_boothpg.split() if i.isdigit()]
                total_page = str(n[1])

                if int(page) <= int(total_page):
                    for obj in pag_num:
                        data1 = {"primary_key": obj.primary_key, "booth_name": obj.booth_name, "status": obj.status, \
                                 "added_datetime": obj.added_datetime, "updated_datetime": obj.updated_datetime}
                        json_data.append(data1)

                    index_page = str(n[0])
                    status = "Success"
                    status_code = 200
                    message = "Successfully received the booth_names"
                else:
                    status = "Failed"
                    message = "Total booth_name pages across the limit"
                    status_code = 407
            else:
                status = "Failed"
                message = "Total booth_name pages beyond the limit"
                status_code = 407
    except Exception as e:
        status = "Failed"
        message = str(e)
        status_code = 409
    return JsonResponse({"status": status, "data": json_data, "message": message,
                         "status_code": status_code, "total_page": total_page, "index_page": index_page})

###Updating_Booth_Names:
@csrf_exempt
def updating_booth_names(request):
    status = ''
    message = ''
    status_code = ''

    try:
        requestData = json.loads(request)
    except:
        requestData = request.POST

    try:
        primary_key = requestData.get(u"primary_key", None)
        state_name = requestData.get(u"state_name", None)
        assembly_name = requestData.get(u"assembly_name", None)
        mandal_name = requestData.get(u"mandal_name", None)
        village_name = requestData.get(u"village_name", None)
        new_booth_name = requestData.get(u"new_booth_name", None)
        new_status = requestData.get(u"new_status", None)
        updated_datetime = datetime.now()


        states = State_Name.objects.get(primary_key=state_name)
        get_assembly = Assembly_Name.objects.get(primary_key=assembly_name, state_name=states)
        get_mandal_name = Mandal_Name.objects.get(primary_key=mandal_name, state_name=states, assembly_name=get_assembly)
        get_village = Village_Name.objects.get(primary_key=village_name, state_name=states, assembly_name=get_assembly,\
                                               mandal_name=get_mandal_name)
        get_booth = Booth_Name.objects.get(primary_key=primary_key, state_name=states, assembly_name=get_assembly,\
                                           mandal_name=get_mandal_name, village_name=get_village)

        if new_booth_name !=None and new_booth_name != "":
            check_booth_names = Booth_Name.objects.filter(booth_name__iexact=new_booth_name)
            if check_booth_names.exists() == False:
                get_booth.booth_name = new_booth_name
                get_booth.status = str2bool(new_status)
                get_booth.updated_datetime = updated_datetime
                get_booth.save()

                status = "Success"
                message = "Successfully updated the booth_name"
                status_code = "200"

            else:
                status = "Failed"
                message = "Booth_Name already exists"
                status_code = 407
        else:
            status = "Failed"
            message = "Booth_Name cannot be empty"
            status_code = 407

    except Exception as e:
        status = "Failed"
        message = str(e)
        status_code = 409
    return JsonResponse({"status": status, "message": message, "status_code": status_code})
