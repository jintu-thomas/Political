from django.shortcuts import render
from .models import Employee,Employee_Login,Employee_Otp
from django.views.decorators.csrf import csrf_exempt
import json
from statusapp.models import Departments,Roles
from django.core.paginator import Paginator
from datetime import datetime
from django.http import JsonResponse
import string
import hashlib
import random
from threading import Timer
import boto3 as boto3



#AWS_SMS_KEYS
client = boto3.client(
    "sns",
    aws_access_key_id="aws_access_key_id",
    aws_secret_access_key="aws_secret_access_key",
    region_name="region_name"
)

host_ip_address = "http://127.0.0.1:8000/media/"

# Create your views here.

@csrf_exempt
def adding_employee(request):
    status = ''
    message = ''
    status_code = ''

    try:
        requestData = json.loads(request.body)
    except:
        requestData = request.POST

    try:
        department = requestData.get(u"department", None)
        role = requestData.get(u"role", None)
        added_by = requestData.get(u"added_by", None)
        firstname = requestData.get(u"firstname", None)
        lastname = requestData.get(u"lastname", None)
        date_of_birth = requestData.get(u"date_of_birth", None)
        birth_place = requestData.get(u"birth_place", None)
        gender = requestData.get(u"gender", None)
        email = requestData.get(u"emailid", None)
        mobile_number = requestData.get(u"mobile_number", None)
        user_role = requestData.get(u"user_role", None)
        employee_id = requestData.get(u"employee_id", None)
        nationality = requestData.get(u"nationality", None)
        community = requestData.get(u"community", None)
        caste = requestData.get(u"caste", None)

        adhaar_card_no = requestData.get(u"adhaar_card_no", None)
        pan_card_no = requestData.get(u"pan_card_no", None)
        voter_id_no = requestData.get(u"voter_id_no", None)
        present_door_no = requestData.get(u"present_door_no", None)
        present_street = requestData.get(u"present_street", None)
        present_locality_name = requestData.get(u"present_locality_name", None)
        present_landmark_name = requestData.get(u"present_landmark_name", None)
        present_city = requestData.get(u"present_city", None)
        present_state = requestData.get(u"present_state", None)
        present_pincode = requestData.get(u"present_pincode", None)
        present_country = requestData.get(u"present_country", None)
        alternate_mobile = requestData.get(u"alternate_mobile", None)
        father_name = requestData.get(u"father_name", None)
        mothers_name = requestData.get(u"mothers_name", None)
        medical_issue = requestData.get(u"medical_issue", None)
        account_status = requestData.get(u"account_status", None)
        registration_status = requestData.get(u"registration_status", None)
        marital_status = requestData.get(u"marital_status", None)
        added_date = datetime.now()

        try:
            departments = Departments.objects.get(primary_key=department)
            get_roles = Roles.objects.get(primary_key=role, department_name=departments)

            Employee.objects.get_or_create(department=departments, role=get_roles, \
                                           added_by=added_by, firstname=firstname, \
                                           lastname=lastname, date_of_birth=date_of_birth, birth_place=birth_place, \
                                           gender=gender, emailid=email, mobile_number=mobile_number,\
                                           user_role=user_role, employee_id=employee_id, nationality=nationality, \
                                           community=community, caste=caste, adhaar_card_no=adhaar_card_no, \
                                           pan_card_no=pan_card_no, voter_id_no=voter_id_no,\
                                           present_door_no=present_door_no, present_street=present_street,\
                                           present_locality_name=present_locality_name, \
                                           present_landmark_name=present_landmark_name, present_city=present_city,\
                                           present_state=present_state, \
                                           present_pincode=present_pincode, present_country=present_country,\
                                           alternate_mobile=alternate_mobile, \
                                           father_name=father_name, mothers_name=mothers_name,\
                                           medical_issue=medical_issue, \
                                           account_status=account_status, registration_status=registration_status,\
                                           marital_status=marital_status, \
                                           added_datetime=added_date)
            status = "Success"
            message = "Employees was created successfully "
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

###uploading_photos
@csrf_exempt
def uploading_employee_photos(request):
    status = ''
    message = ''
    status_code = ''

    try:
        requestData = json.loads(request.body)
    except:
        requestData = request.POST

    try:
        department = requestData.get(u"department", None)
        role = requestData.get(u"role", None)
        employee_uuid = requestData.get(u"employee_uuid", None)

        departments = Departments.objects.get(primary_key=department)
        get_roles = Roles.objects.get(primary_key=role, department_name=departments)
        employee = Employee.objects.get(employee_uuid=employee_uuid, department=departments, role=get_roles)

        user_picture = None
        adhaar_card_pic_front = None
        adhaar_card_pic_back = None
        pan_card_pic_front = None
        pan_card_pic_back = None
        voter_id_pic_front = None
        voter_id_pic_back = None

        if "user_picture" in request.FILES:
            user_picture = request.FILES['user_picture']
            employee.user_picture = user_picture

        if "adhaar_card_pic_front" in request.FILES:
            adhaar_card_pic_front = request.FILES['adhaar_card_pic_front']
            employee.adhaar_card_pic_front = adhaar_card_pic_front

        if "adhaar_card_pic_back" in request.FILES:
            adhaar_card_pic_back = request.FILES['adhaar_card_pic_back']
            employee.adhaar_card_pic_back = adhaar_card_pic_back

        if "pan_card_pic_front" in request.FILES:
            pan_card_pic_front = request.FILES['pan_card_pic_front']
            employee.pan_card_pic_front = pan_card_pic_front

        if "pan_card_pic_back" in request.FILES:
            pan_card_pic_back = request.FILES['pan_card_pic_back']
            employee.pan_card_pic_back = pan_card_pic_back

        if "voter_id_pic_front" in request.FILES:
            voter_id_pic_front = request.FILES['voter_id_pic_front']
            employee.voter_id_pic_front = voter_id_pic_front

        if "voter_id_pic_back" in request.FILES:
            voter_id_pic_back = request.FILES['voter_id_pic_back']
            employee.voter_id_pic_back = voter_id_pic_back

        employee.save()
        status = "Success"
        message = "Successfully upload the employee photos"
        status_code = 200

    except Exception as e:
        status = "Failed"
        message = str(e)
        status_code = 404
    return JsonResponse({"status": status, "message": message, "status_code": status_code})

##getting_employees
@csrf_exempt
def getting_employees(request):
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
        department = requestData.get(u"department")
        role = requestData.get(u"role", None)

        departments = Departments.objects.get(primary_key=department)
        get_roles = Roles.objects.get(primary_key=role, department_name=departments)
        total_employees = Employee.objects.filter(department=departments, role=get_roles)

        if total_employees.exists():
            roles_paginator = Paginator(total_employees, 10)
            if int(page) > 0:
                pag_num = roles_paginator.get_page(page)
                n_employeepg = str(pag_num)[1:-1]
                n = [int(i) for i in n_employeepg.split() if i.isdigit()]
                total_page = str(n[1])

                if int(page) <= int(total_page):
                    for obj in pag_num:
                        data1 = {"employee_uuid": obj.employee_uuid,\
                                 "added_by": obj.added_by, "firstname": obj.firstname, "lastname": obj.lastname,\
                                 "date_of_birth": obj.date_of_birth, "birth_place": obj.birth_place,\
                                 "gender": obj.gender,"emailid": obj.emailid, "mobile_number": obj.mobile_number,\
                                 "picture": str(obj.user_picture), "user_role": obj.user_role, "employee_id": obj.employee_id,\
                                 "nationality": obj.nationality, "community": obj.community, "caste": obj.caste,\
                                 "adhaar_card_no": obj.adhaar_card_no, "adhaar_card_front": str(obj.adhaar_card_pic_front),\
                                 "adhaar_card_back": str(obj.adhaar_card_pic_back),\
                                 "pan_card_no": obj.pan_card_no, "pan_card_front": str(obj.pan_card_pic_front),\
                                 "pan_card_back": str(obj.pan_card_pic_back),\
                                 "voter_id_no": obj.voter_id_no, "voter_id_front": str(obj.voter_id_pic_front),\
                                 "voter_id_pic_back": str(obj.voter_id_pic_back),\
                                 "present_door_no": obj.present_door_no, "present_street": obj.present_street, "present_locality_name": obj.present_locality_name,\
                                 "present_landmark_name": obj.present_landmark_name, "present_city": obj.present_city, "present_state": obj.present_state,\
                                 "father_name": obj.father_name, "mothers_name": obj.mothers_name ,"medical_issue": obj.medical_issue,\
                                 "present_pincode": obj.present_pincode, "present_country": obj.present_country,\
                                 "account_status": obj.account_status, "registration_status": obj.registration_status, "marital_status": obj.marital_status,\
                                 "added_datetime": obj.added_datetime, "updated_datetime": obj.updated_datetime\
                                 }
                        json_data.append(data1)

                    index_page = str(n[0])
                    status = "Success"
                    message = "Successfully received the employees"
                    status_code = 200
                else:
                    status = "Failed"
                    message = "Total employees pages across the limit"
                    status_code = 409
            else:
                status = "Failed"
                message = "Total employees pages beyond the limit"
                status_code = 409

    except Exception as e:
        status = "Failed"
        message = str(e)
        status_code = 400
    return JsonResponse({"status": status, "data": json_data, "message": message,\
                         "status_code": status_code, "total_page": total_page, "index_page": index_page})


###updating_employee_details:
@csrf_exempt
def updating_employees(request):
    status = ''
    message = ''
    status_code = ''

    try:
        requestData = json.loads(request.body)
    except:
        requestData = request.POST
    try:
        employee_uuid = requestData.get(u"employee_uuid", None)
        department = requestData.get(u"department", None)
        role = requestData.get(u"role", None)
        new_firstname = requestData.get(u"new_firstname", None)
        new_lastname = requestData.get(u"new_lastname", None)
        new_date_of_birth = requestData.get(u"new_date_of_birth", None)
        new_birth_place = requestData.get(u"new_birth_place", None)
        new_gender = requestData.get(u"new_gender", None)
        new_emailid = requestData.get(u"new_emailid", None)
        new_mobile_number = requestData.get(u"new_mobile_number", None)
        new_user_role = requestData.get(u"new_user_role", None)
        new_employee_id = requestData.get(u"new_employee_id", None)
        new_nationality = requestData.get(u"new_nationality", None)
        new_community = requestData.get(u"new_community", None)
        new_caste = requestData.get(u"new_caste", None)

        new_adhaar_card_no = requestData.get(u"new_adhaar_card_no", None)
        new_pan_card_no = requestData.get(u"new_pan_card_no", None)
        new_voter_id_no = requestData.get(u"new_voter_id_no", None)
        new_present_door_no = requestData.get(u"new_present_door_no", None)
        new_present_street = requestData.get(u"new_present_street", None)
        new_present_locality_name = requestData.get(u"new_present_locality_name", None)
        new_present_landmark_name = requestData.get(u"new_present_landmark_name", None)
        new_present_city = requestData.get(u"new_present_city", None)
        new_present_state = requestData.get(u"new_present_state", None)
        new_present_pincode = requestData.get(u"new_present_pincode", None)
        new_present_country = requestData.get(u"new_present_country", None)
        new_alternate_mobile = requestData.get(u"new_alternate_mobile", None)
        new_father_name = requestData.get(u"new_father_name", None)
        new_mothers_name = requestData.get(u"new_mothers_name", None)
        new_medical_issue = requestData.get(u"new_medical_issue", None)
        new_account_status = requestData.get(u"new_account_status", None)
        new_registration_status = requestData.get(u"new_registration_status", None)
        new_marital_status = requestData.get(u"new_marital_status", None)
        updated_datetime = datetime.now()

        try:
            departments = Departments.objects.get(primary_key=department)
            get_roles = Roles.objects.get(primary_key=role, department_name=departments)
            get_employees = Employee.objects.get(employee_uuid=employee_uuid, department=departments, role=get_roles)

            if new_firstname != None and new_firstname != "":
                get_employees.firstname = new_firstname

            if new_lastname != None and new_lastname != "":
                get_employees.lastname = new_lastname

            if new_date_of_birth != None and new_date_of_birth != "":
                get_employees.date_of_birth = new_date_of_birth

            if new_birth_place != None and new_birth_place != "":
                get_employees.birth_place = new_birth_place

            if new_gender != None and new_gender != "":
                get_employees.gender = new_gender

            if new_emailid != None and new_emailid != "":
                get_employees.emailid = new_emailid

            if new_mobile_number != None and new_mobile_number != "":
                get_employees.mobile_number = new_mobile_number

            if new_user_role != None and new_user_role != "":
                get_employees.user_role = new_user_role

            if new_employee_id != None and new_employee_id != "":
                get_employees.employee_id = new_employee_id

            if new_nationality != None and new_nationality != "":
                get_employees.nationality = new_nationality

            if new_community != None and new_community != "":
                get_employees.community = new_community

            if new_caste != None and new_caste != "":
                get_employees.caste = new_caste

            if new_adhaar_card_no != None and new_adhaar_card_no != "":
                get_employees.adhaar_card_no = new_adhaar_card_no

            if new_pan_card_no != None and new_pan_card_no != "":
                get_employees.pan_card_no = new_pan_card_no

            if new_voter_id_no != None and new_voter_id_no != "":
                get_employees.voter_id_no = new_voter_id_no

            if new_present_door_no != None and new_present_door_no != "":
                get_employees.present_door_no = new_present_door_no

            if new_present_street != None and new_present_street != "":
                get_employees.present_street = new_present_street

            if  new_present_locality_name != None and new_present_locality_name != "":
                get_employees.present_locality_name = new_present_locality_name

            if new_present_landmark_name != None and new_present_landmark_name != "":
                get_employees.present_landmark_name = new_present_landmark_name

            if new_present_city != None and new_present_city != "":
                get_employees.present_city = new_present_city

            if new_present_state != None and new_present_state != "":
                get_employees.present_state = new_present_state

            if new_present_pincode != None and new_present_pincode != "":
                get_employees.present_pincode = new_present_pincode

            if new_present_country != None and new_present_country != "":
                get_employees.present_country = new_present_country

            if new_alternate_mobile != None and new_alternate_mobile != "":
                get_employees.alternate_mobile = new_alternate_mobile

            if new_father_name != None and new_father_name != "":
                get_employees.father_name = new_father_name

            if new_mothers_name != None and new_mothers_name != "":
                get_employees.mothers_name = new_mothers_name

            if new_medical_issue != None and new_medical_issue != "":
                get_employees.medical_issue = new_medical_issue

            if new_medical_issue != None and new_medical_issue != "":
                get_employees.medical_issue = new_medical_issue

            if new_account_status != None and new_account_status != "":
                get_employees.account_status = new_account_status

            if new_registration_status != None and new_registration_status != "":
                get_employees.registration_status = new_registration_status

            if new_marital_status != None and new_marital_status != "":
                get_employees.marital_status = new_marital_status
                get_employees.updated_datetime = updated_datetime

            get_employees.save()

            status = "Success"
            message = "Employee personal details was successfully updated"
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

###updating_employee_photos:
@csrf_exempt
def updating_employee_photos(request):
    status = ''
    message = ''
    status_code = ''

    try:
        requestData = json.loads(request.body)
    except:
        requestData = request.POST

    try:
        employee_uuid = requestData.get(u"employee_uuid", None)
        department = requestData.get(u"department", None)
        role = requestData.get(u"role", None)

        new_user_picture = None
        new_adhaar_card_pic_front = None
        new_adhaar_card_pic_back = None
        new_pan_card_pic_front = None
        new_pan_card_pic_back = None
        new_voter_id_pic_front = None
        new_voter_id_pic_back = None

        try:
            departments = Departments.objects.get(primary_key=department)
            get_roles = Roles.objects.get(primary_key=role, department_name=departments)
            employee = Employee.objects.get(employee_uuid=employee_uuid, department=departments, role=get_roles)

            if "new_user_picture" in request.FILES:
                new_user_picture = request.FILES['new_user_picture']
                employee.user_picture = new_user_picture

            if "new_adhaar_card_pic_front" in request.FILES:
                new_adhaar_card_pic_front = request.FILES['new_adhaar_card_pic_front']
                employee.adhaar_card_pic_front = new_adhaar_card_pic_front

            if "new_adhaar_card_pic_back" in request.FILES:
                new_adhaar_card_pic_back = request.FILES['new_adhaar_card_pic_back']
                employee.adhaar_card_pic_back = new_adhaar_card_pic_back

            if "new_pan_card_pic_front" in request.FILES:
                new_pan_card_pic_front = request.FILES['new_pan_card_pic_front']
                employee.pan_card_pic_front = new_pan_card_pic_front

            if "new_pan_card_pic_back" in request.FILES:
                new_pan_card_pic_back = request.FILES['new_pan_card_pic_back']
                employee.pan_card_pic_back = new_pan_card_pic_back

            if "new_voter_id_pic_front" in request.FILES:
                new_voter_id_pic_front = request.FILES['new_voter_id_pic_front']
                employee.voter_id_pic_front = new_voter_id_pic_front

            if "new_voter_id_pic_back" in request.FILES:
                new_voter_id_pic_back = request.FILES['new_voter_id_pic_back']
                employee.voter_id_pic_back = new_voter_id_pic_back

            employee.save()
            status = "Success"
            message = "Successfully updated the employee photos"
            status_code = 200

        except Exception as e:
            import traceback
            traceback.print_exc()
            status = "Failed"
            message = str(e)
            status_code = 409

    except Exception as e:
        import traceback
        traceback.print_exc()
        status = "Failed"
        message = str(e)
        status_code = 409
    return JsonResponse({"status": status, "message": message, "status_code": status_code})

###creating_employee_login:
@csrf_exempt
def creating_employee_login(request):
    status = ''
    message = ''
    status_code = ''

    try:
        requestData = json.loads(request.body)
    except:
        requestData = request.POST
    try:
        employee_uuid = requestData.get(u"employee_uuid", None)
        mobile_number = requestData.get(u"mobile_number", None)

        try:
            employee = Employee.objects.get(employee_uuid=employee_uuid, mobile_number=mobile_number)
            chars = string.ascii_letters + string.digits
            emp_password = ''.join(random.choice(chars) for _ in range(8))
            encode_password = hashlib.md5(emp_password.encode())
            hash_password = encode_password.hexdigest()

            try:
                message = " Hii The credentials for login to the Political App is, Employee ID is  "+mobile_number+", The login credentials for the  political password "+emp_password+",is successfully created.Please don't share this credentials with any unauthorised person."
                send_sms = client.publish(
                    PhoneNumber="+91" + str(mobile_number),
                    Message=message,
                    MessageAttributes={'AWS.SNS.SMS.SenderID': {'DataType': 'String', 'StringValue': 'VARPAT'},
                                       'AWS.SNS.SMS.SMSType': {'DataType': 'String', 'StringValue': 'Transactional'}}
                )
                ResponseMetadata = send_sms.get('ResponseMetadata')
                print(ResponseMetadata)
                request_status_code = ResponseMetadata.get('HTTPStatusCode')

                if request_status_code == 200:
                    print("Message sent successfully")
                    Employee_Login.objects.get_or_create(employee_uuid=employee, password=hash_password)

                    status = "Success"
                    message = "Successfully employee login was created"
                    status_code = 200
                else:
                    status = "Failed"
                    message = "Failed to send the message"
                    status_code = 403

            except Exception as e:
                status = "Failed"
                message = str(e)
                status_code = 404

        except Exception as e:
            status = "Failed"
            message = str(e)
            status_code = 404

    except Exception as e:
        status = "Failed"
        message = str(e)
        status_code = 400
    return JsonResponse({"status": status, "message": message, "status_code": status_code})

###employee_login
@csrf_exempt
def employee_login(request):
    status = ''
    message = ''
    json_data = []
    data = dict()
    status_code = ''

    try:
        requestData = json.loads(request.body)
    except:
        requestData = request.POST

    try:
        employee_uuid = requestData.get(u"employee_uuid", None)
        mobile_number = requestData.get(u"mobile_number", None)
        password = requestData.get(u"password", None)
        loginTime = datetime.now()
        encode_password = hashlib.md5(password.encode())
        hash_password = encode_password.hexdigest()

        try:
            get_employee = Employee_Login.objects.get(employee_uuid=employee_uuid)
            employee_password = get_employee.password

            try:

                print(get_employee.employee_uuid)
                employee = Employee.objects.get(employee_uuid=get_employee.employee_uuid.employee_uuid, mobile_number=mobile_number)

                if employee_password == hash_password:
                    lastLoginTime = get_employee.lastLogin
                    lastPasswordUpdated = get_employee.lastPasswordUpdated

                    get_employee.lastLogin = loginTime

                    get_employee.save()


                    data1={
                         "mobile_no": employee.mobile_number,
                         "lastLogin": lastLoginTime,
                         "lastPasswordUpdated": lastPasswordUpdated}
                    json_data.append(data1)

                    status = "Success"
                    message = "Successfully employee login into the account"
                    status_code = 200
                else:
                    status = "Wrong password"
                    status_code = 401

            except Exception as e:
                status = "Failed"
                message = str(e)
                status_code = 403

        except Exception as e:
            status = "Failed"
            message = str(e)
            status_code = 404

    except Exception as e:
        status = "Failed"
        message = str(e)
        status_code = 400
    return JsonResponse({"status": status, "message": message, "data": json_data, "status_code":status_code})

###employee_forgot_password:
@csrf_exempt
def employee_forgot_password(request):
    status = ''
    message = ''
    status_code = ''
    try:
        requestData = json.loads(request.body)
    except:
        requestData = request.POST
    try:
        mobile_number = requestData.get(u"mobile_number", None)
        employee = Employee.objects.get(mobile_number=mobile_number)
        role = "Employee"

        try:
            send_otp = generate_otp(employee, role)

            if send_otp == "Success":
                status = "Success"
                message = "Successfully otp received"
                status_code = 200
            else:
                status = "Error in sending OTP"
                status_code = 500

        except Exception as e:
            status = "Failed"
            message = str(e)
            status_code = 409

    except Exception as e:
        status = "Failed"
        message = str(e)
        status_code = 409
    return JsonResponse({"status": status, "message": message, "status_code": status_code})

###genearte_otp password:
def generate_otp(employee_user, role):
    global mobile_number
    status = ''

    if role == "Employee":
        mobile_number = employee_user.mobile_number

    try:
        digits = string.digits
        otp = ''.join(random.choice(digits) for _ in range(4))
        message = "Your One Time Password for Political App is " + str(
            otp) + ". OTP is valid only for 5 minutes. Please ignore this if you have not requested."

        send_sms = client.publish(
            PhoneNumber="+91" + str(mobile_number),
            Message=message,
            MessageAttributes={'AWS.SNS.SMS.SenderID': {'DataType': 'String', 'StringValue': 'VARPAT'},
                               'AWS.SNS.SMS.SMSType': {'DataType': 'String', 'StringValue': 'Transactional'}}
        )

        ResponseMetadata = send_sms.get('ResponseMetadata')
        print(ResponseMetadata)
        request_status_code = ResponseMetadata.get('HTTPStatusCode')

        if request_status_code == 200:
            print("Message sent successfully")

            if role == "Employee":
                Employee_Otp.objects.update_or_create(mobile_number=employee_user, defaults={'mobile_otp': otp})

                data = [employee_user]
                time = Timer(300.0, delete_employee_otp, data)
                time.start()

            status = "Success"
        else:
            status = "Failed"
    except:
        status = 'Failed'

    return status

    

###Delete employee OTP after 5 mins
def delete_employee_otp(data1):
    check_employee_otp = Employee_Otp.objects.get(mobile_number=data1)
    check_employee_otp.delete()

###employee_otp_verifing:
@csrf_exempt
def employee_otp_verifying(request):
    status = ''
    message = ''
    json_data = []
    data = dict()
    status_code = ''

    try:
        requestData = json.loads(request.body)
    except:
        requestData = request.POST
    try:
        mobile_number = requestData.get(u"mobile_number", None)
        otp_password = requestData.get(u"otp_password", None)

        try:
            check_employee = Employee_Otp.objects.get(mobile_number__mobile_number=mobile_number)
            check_otp = check_employee.mobile_otp

            if check_otp == otp_password:
                employee = Employee.objects.get(mobile_number=mobile_number)
                data1 = {
                    "mobile_number": employee.mobile_number
                }
                json_data.append(data1)

                status = "Success"
                message = "Successfully mobile_otp verified"
                status_code = 200

            else:
                status = "Wrong OTP"
                status_code = 401

        except Exception as e:
            status = "Failed"
            message = str(e)
            status_code = 409

    except Exception as e:
        status = "Failed"
        message = str(e)
        status_code = 409
    return JsonResponse({"status": status, "message": message, "data": json_data,"status_code": status_code})


###employee_changing_password:
@csrf_exempt
def employee_changing_password(request):
    status = ''
    message = ''
    status_code = ''

    try:
        requestData = json.loads(request.body)
    except:
        requestData = request.POST

    try:
        mobile_number = requestData.get(u"mobile_number", None)
        old_password = requestData.get(u"old_password", None)
        new_password = requestData.get(u"new_password", None)
        updatedTime = datetime.now()

        old_password = hashlib.md5(old_password.encode())
        old_password = old_password.hexdigest()

        new_password = hashlib.md5(new_password.encode())
        new_password = new_password.hexdigest()

        try:

            employee_check = Employee.objects.get(mobile_number=mobile_number)
            check_employee = Employee_Login.objects.get(employee_uuid=employee_check, password=old_password)

            if new_password != None:
                check_employee.password = new_password
            if updatedTime != None:
                check_employee.lastPasswordUpdated = updatedTime
                check_employee.save()

            status = "Success"
            message = "Successfully for your Political App password was changed"
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
