from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
# import datetime
from datetime import datetime
from .models import Departments,Roles
from str2bool import str2bool
from django.http import JsonResponse
import ast
from django.core.paginator import Paginator

# Create your views here.

@csrf_exempt
def adding_departments(request):
    status = ''
    message = ''
    status_code = ''

    try:
        requestData = json.loads(request.body)
    except:
        requestData = request.POST

    try:
        departments_name = requestData.get(u"departments_name", None)
        added_by = requestData.get(u"added_by", None)
        added_date = datetime.now()

        # [{"name":"Android","status":"true"}, {"name":"Web","status":"true"}]
        departments_name = ast.literal_eval(str(departments_name))             

        try:
            for i in departments_name:
            #for i in jintu
                Departments.objects.get_or_create(department_name=(i['name']),\
                                                defaults={'status': str2bool(i['status']), 'added_by': added_by,
                                                            'added_datetime': added_date})
                #checking department_name is already exist
                status = "Success"
                message = "Successfully Departments created"
                status_code = 200
        except Exception as e:
            import traceback
            traceback.print_exc()
            status = "Failed"
            message = str(e)
            status_code = 400

    except Exception as e:
        status = "Failed"
        message = str(e)
        status_code = 400
    return JsonResponse({"status": status, "message": message, "status_code": status_code})

@csrf_exempt
def getting_departments(request):
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
        total_departments = Departments.objects.all()

        if total_departments.exists():
            departments_paginator = Paginator(total_departments, 10)
            if int(page) > 0:
                pag_num = departments_paginator.get_page(page)
                n_deppg = str(pag_num)[1:-1]
                n = [int(i) for i in n_deppg.split() if i.isdigit()]
                total_page = str(n[1])

                if int(page) <= int(total_page):
                    for obj in pag_num:
                        data1 = {"primary_key": obj.primary_key, "department_name": obj.department_name,\
                                 "status": obj.status,\
                                 "added_by": obj.added_by, "added_datetime": obj.added_datetime,\
                                 "updated_datetime": obj.updated_datetime}
                        json_data.append(data1)

                    index_page = str(n[0])
                    status = "Success"
                    message = "Successfully received the departments"
                    status_code = 200
                else:
                    status = "Failed"
                    message = "Total department pages across the limit"
                    status_code = 409
            else:
                status = "Failed"
                message = "Total department pages beyond the limit"
                status_code = 409
    except Exception as e:
        status = "Failed"
        message = str(e)
        status_code = 404
    return JsonResponse({"status": status, "data": json_data, "message": message, \
                         "status_code": status_code, "total_page": total_page, "index_page": index_page})

###updating departments
@csrf_exempt
def updating_departments(request):
    status = ''
    message = ''
    status_code = ''

    try:
        requestData = json.loads(request.body)
    except:
        requestData = request.POST

    try:
        primary_key = requestData.get(u"primary_key", None)
        new_department_name = requestData.get(u"new_department_name", None)
        new_status = requestData.get(u"new_status", None)
        updated_datetime = datetime.now()

        try:
            get_departments = Departments.objects.get(primary_key=primary_key)

            if new_department_name != None and new_department_name != "":
                check_department = Departments.objects.filter(department_name__iexact=new_department_name)
                                                            #(department_name__iexact = "jintu")
                
                if check_department.exists() == False:
                    #jintu in not there 
                    get_departments.department_name = new_department_name
                    get_departments.status = str2bool(new_status)
                    get_departments.updated_datetime = updated_datetime
                    get_departments.save()

                    status = "Success"
                    message = "Department details updated successfully"
                    status_code = 200
                else:
                    status = "Failed"
                    message = "Department name already exists"
                    status_code = 409
            else:
                status = "Failed"
                message = "Department name cannot be empty"
                status_code = 403
        except Exception as e:
            status = "Failed"
            message = str(e)
            status_code = 400
    except Exception as e:
        status = "Failed"
        message = str(e)
        status_code = 400
    return JsonResponse({"status": status, "message": message, "status_code": status_code})

###adding roles
@csrf_exempt
def adding_roles(request):
    status = ''
    message = ''
    status_code = ''

    try:
        requestData = json.loads(request.body)
    except:
        requestData = request.POST

    try:
        department_name = requestData.get(u"department_name", None)
        role_name = requestData.get(u"role_name", None)
        added_by = requestData.get(u"added_by", None)
        added_date = datetime.now()

        # [{"name":"Role","status":"true"}, {"name":"Role1","status":"true"}]
        role_name = ast.literal_eval(str(role_name))
        try:
            departments = Departments.objects.get(primary_key=department_name)
            for i in role_name:
                Roles.objects.get_or_create(department_name=departments, \
                                            role_name=(i['name']), \
                                            defaults={'status': str2bool(i['status']), 'added_by': added_by,
                                                      'added_datetime': added_date})
                status = "Success"
                message = "Roles was created successfully"
                status_code = 200
        except Exception as e:
            status = "Failed"
            message = str(e)
            status_code = 404
    except Exception as e:
        status = "Failed"
        message = str(e)
        status_code = 404
    return JsonResponse({"status": status, "message": message, "status_code": status_code})

###getting roles
@csrf_exempt
def getting_roles(request):
    status = ''
    message = ''
    status_code = ''
    index_page = ''
    total_page = ''
    json_data = []
    data = dict()

    try:
        requestData = json.loads(request.body)
    except:
        requestData = request.POST
    try:
        page = requestData.get(u"page", None)
        department_name = requestData.get(u"department_name")

        departments = Departments.objects.get(primary_key=department_name)
        total_roles = Roles.objects.filter(department_name=departments)

        if total_roles.exists():
            roles_paginator = Paginator(total_roles, 10)
            if int(page) > 0:
                pag_num = roles_paginator.get_page(page) #page = 1,2,3,4... whatever
                n_rolepg = str(pag_num)[1:-1]
                # print("n_rolepg:"n_rolepg) -> o/p n_rolepg: input_page of total page
                n = [int(i) for i in n_rolepg.split() if i.isdigit()]
                total_page = str(n[1])

                if int(page) <= int(total_page):
                    for obj in pag_num:
                        data1 = {"primary_key": obj.primary_key,\
                                 "role_name": obj.role_name, "status": obj.status, "added_by": obj.added_by,\
                                 "added_datetime": obj.added_datetime, "updated_datetime": obj.updated_datetime}
                        json_data.append(data1)

                    index_page = str(n[0])
                    status = "Success"
                    message = "Successfully received the roles"
                    status_code = 200
                else:
                    status = "Failed"

                    message = "Total roles pages across the limit"
                    status_code = 409
            else:
                status = "Failed"
                message = "Total roles pages beyond the limit"
                status_code = 409

    except Exception as e:
        status = "Failed"
        message = str(e)
        status_code = 400
    return JsonResponse({"status": status, "data": json_data, "message": message, \
                         "status_code": status_code, "total_page": total_page, "index_page": index_page})

###update the roles
@csrf_exempt
def updating_roles(request):
    status = ''
    message = ''
    status_code = ''
    try:
        requestData = json.loads(request.body)
    except:
        requestData = request.POST
    try:
        primary_key = requestData.get(u"primary_key", None)
        department_name = requestData.get(u"department_name", None)
        new_role_name = requestData.get(u"new_role_name", None)
        new_status = requestData.get(u"status", None)
        updated_datetime = datetime.now()

        try:
            departments = Departments.objects.get(primary_key=department_name)
            get_roles = Roles.objects.get(primary_key=primary_key, department_name=departments)

            if new_role_name != None and new_role_name != "":
                check_role = Roles.objects.filter(role_name__iexact=new_role_name) #check the new_role name is exist or not
                if check_role.exists() == False: #if exist is FAlse value . mean not exist the new role name . It will update with new value
                    get_roles.role_name = new_role_name
                    get_roles.status = str2bool(new_status)
                    get_roles.updated_datetime = updated_datetime
                    get_roles.save()

                    status = "Success"
                    message = "Successfully update the roles"
                    status_code = 200
                else:
                    status = "Failed"
                    message = "Roles name already exists"
                    status_code = 409
            else:
                status = "Failed"
                message = "Roles name can not be empty"
                status_code = 403

        except Exception as e:
            status = "Failed"
            message = str(e)
            status_code = 400
    except Exception as e:
        status = "Failed"
        message = str(e)
        status_code = 400
    return JsonResponse({"status": status, "message": message, "status_code": status_code})
