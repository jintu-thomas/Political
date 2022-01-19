from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
from str2bool import str2bool
from .models import State_Name,Assembly_Name
import ast
from django.http import JsonResponse
from django.core.paginator import Paginator
# Create your views here.

###adding_state_name:
@csrf_exempt
def adding_state_name(request):
    status = ''
    message = ''
    status_code = ''

    try:
        requestData = json.loads(request.body)
    except:
        requestData = request.POST
    try:
        state_name = requestData.get(u"state_name", None)
        state_code = requestData.get(u"state_code", None)
        added_date = datetime.now()

        #[{"name":"AndhraPradesh","status":"true"}]
        state_name = ast.literal_eval(str(state_name))

        try:
            for i in state_name:
                State_Name.objects.get_or_create(state_name=(i['name']),\
                                                 defaults={'status': str2bool(i['status']), 'state_code': state_code,\
                                                           'added_datetime': added_date})
                status = "Success"
                message = "Successfully state_name was created"
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

###getting_state_names:
@csrf_exempt
def getting_state_names(request):
    status = ''
    message = ''
    status_code = ''
    total_page = ''
    index_page = ''
    json_data = []
    data = dict()

    try:
        requestData = json.loads(request.boday)
    except:
        requestData = request.POST
    try:
        page = requestData.get(u"page", None)
        total_states = State_Name.objects.all()

        if total_states.exists():
            states_paginator = Paginator(total_states, 10)
            if int(page) > 0:
                pag_num = states_paginator.get_page(page)
                n_states_pg = str(pag_num)[1:-1]
                n = [int(i) for i in n_states_pg.split() if i.isdigit()]
                total_page = str(n[1])

                if int(page) <= int(total_page):
                    for obj in pag_num:
                        data1 = {"primary_key": obj.primary_key, "state_name": obj.state_name,\
                                 "state_code": obj.state_code, "status": obj.status,\
                                 "added_datetime": obj.added_datetime, "updated_datetime": obj.updated_datetime}
                        json_data.append(data1)

                    index_page = str(n[0])
                    status = "Success"
                    message = "Successfully received sate_names"
                    status_code = 200
                else:
                    status = "Failed"
                    message = "Total state_name pages across the limit"
                    status_code = 407
            else:
                status = "Failed"
                message = "Total state_name pages beyond the limit"
                status_code = 407

    except Exception as e:
        status = "Failed"
        message = str(e)
        status_code = 409
    return JsonResponse({"status": status, "data": json_data, "message": message,
                         "status_code": status_code, "total_page": total_page, "index_page": index_page})

###updating_state_names:
@csrf_exempt
def updating_state_names(request):
    status = ''
    message = ''
    status_code = ''
    try:
        requestData = json.loads(request.body)
    except:
        requestData = request.POST
    try:
        primary_key = requestData.get(u"primary_key", None)
        new_state_name = requestData.get(u"new_state_name", None)
        new_state_code = requestData.get(u"new_state_code", None)
        new_status = requestData.get(u"new_status", None)
        updated_datetime = datetime.now()

        try:
            get_state_name = State_Name.objects.get(primary_key=primary_key)

            if new_state_name != None and new_state_name != "":
                check_state_name = State_Name.objects.filter(state_name__iexact=new_state_name)
                if check_state_name.exists() == False:

                    get_state_name.state_name = new_state_name
                    get_state_name.state_code = new_state_code
                    get_state_name.status = str2bool(new_status)
                    get_state_name.updated_datetime = updated_datetime
                    get_state_name.save()

                    status = "Success"
                    message = "Successfully updated the state_names"
                    status_code = 200
                else:
                    status = "Failed"
                    message = "state_names already exists"
                    status_code = 407
            else:
                status = "Failed"
                message = "state_names cannot be empty"
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


#------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------

###Addinng_Assembly_Name:
@csrf_exempt
def adding_assembly_name(request):
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
        added_date = datetime.now()

        # [{"name":"AndhraPradesh","status":"true"}]
        assembly_name = ast.literal_eval(str(assembly_name))
        try:
            states = State_Name.objects.get(primary_key=state_name)
            for i in assembly_name:
                Assembly_Name.objects.get_or_create(state_name=states, assembly_name=(i['name']),\
                                                    defaults={'status': str2bool(i['status']), 'added_datetime': added_date})
                status = "Success"
                message = "Successfully assembly_name was created"
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

###getting_Assembly_Names:
@csrf_exempt
def getting_assembly_names(request):
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

        try:
            states = State_Name.objects.get(primary_key=state_name)
            total_assembly = Assembly_Name.objects.filter(state_name=states)

            if total_assembly.exists():
                assembly_paginator = Paginator(total_assembly, 10)
                if int(page) > 0:
                    pag_num = assembly_paginator.get_page(page)
                    n_assembly_pg = str(pag_num)[1:-1]
                    n = [int(i) for i in n_assembly_pg.split() if i.isdigit()]
                    total_page = str(n[1])

                    if int(page) <= int(total_page):
                        for obj in pag_num:
                            data1 = {"primary_key": obj.primary_key, "assembly_name": obj.assembly_name,
                                     "status": obj.status, "added_datetime": obj.added_datetime, "updated_datetime": obj.updated_datetime}
                            json_data.append(data1)

                        index_page = str(n[0])
                        status = "Success"
                        message = "Successfully assembly_names received"
                        status_code = 200
                    else:
                        status = "Failed"
                        message = "Total assembly_name pages across the limit"
                        status_code = 407
                else:
                    status = "Failed"
                    message = "Total assembly_name pages beyond the limit"
                    status_code = 407

        except Exception as e:
            status = "Failed"
            message = str(e)
            status_code = 409

    except Exception as e:
        status = "Failed"
        message = str(e)
        status_code = 409
    return JsonResponse({"status": status, "data": json_data, "message": message,
                         "status_code": status_code, "total_page": total_page, "index_page": index_page})

###updating_assembly_names:
@csrf_exempt
def updating_assembly_names(request):
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
        new_assembly_name = requestData.get(u"new_assembly_name", None)
        new_status = requestData.get(u"new_status", None)
        updated_datetime = datetime.now()

        try:
            states = State_Name.objects.get(primary_key=state_name)
            get_assembly_names = Assembly_Name.objects.get(primary_key=primary_key, state_name=states)

            if new_assembly_name != None and new_assembly_name != "":
                check_assembly_names = Assembly_Name.objects.filter(assembly_name__iexact=new_assembly_name)
                if check_assembly_names.exists() == False:
                    get_assembly_names.assembly_name = new_assembly_name
                    get_assembly_names.status = str2bool(new_status)
                    get_assembly_names.updated_datetime = updated_datetime
                    get_assembly_names.save()

                    status = "Success"
                    message = "Successfully update the assembly_names"
                    status_code = 200

                else:
                    status = "Failed"
                    message = "Assembly names already exists"
                    status_code = 407
            else:
                status = "Failed"
                message = "Assembly names can not be empty"
                status_code = 407

        except Exception as e:
            status = 'Failed'
            message = str(e)
            status_code = 409

    except Exception as e:
        status = 'Failed'
        message = str(e)
        status_code = 409
    return JsonResponse({"status": status, "message": message, "status_code": status_code})
