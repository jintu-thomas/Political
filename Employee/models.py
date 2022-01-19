from django.db import models
from statusapp.models import Departments,Roles
import uuid


# Create your models here.

class Employee(models.Model):
    employee_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department = models.ForeignKey(Departments, on_delete=models.SET_NULL, blank=True, null=True)
    role = models.ForeignKey(Roles, on_delete=models.SET_NULL, blank=True, null=True)
    added_by = models.CharField(max_length=128, null=True, blank=True)
    firstname = models.CharField(max_length=64)
    lastname = models.CharField(max_length=64, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    birth_place = models.CharField(max_length=128, null=True, blank=True)
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
        ('Not mentioned', 'Not mentioned'))
    gender = models.CharField(default='Not mentioned', max_length=16, choices=GENDER_CHOICES, null=True, blank=True)
    emailid = models.EmailField(null=True, blank=True)
    mobile_number = models.BigIntegerField(unique=True)
    user_picture = models.FileField(upload_to='Political/User/Profile/', null=True, blank=True)
    ROLE_CHOICES = (
        ('Master Admin', 'Master Admin'),
        ('Employee', 'Employee'),
        ('Admin', 'Admin'))
    user_role = models.CharField(default='Employee', max_length=16, choices=ROLE_CHOICES)
    employee_id = models.CharField(max_length=20, null=True, blank=True)
    nationality = models.CharField(max_length=32, null=True, blank=True)
    community = models.CharField(max_length=64, null=True, blank=True)
    caste = models.CharField(max_length=64, null=True, blank=True)

    adhaar_card_no = models.CharField(max_length=20, null=True, blank=True)
    adhaar_card_pic_front = models.FileField(upload_to='Political/User/adhaar_cards/', null=True, blank=True)
    adhaar_card_pic_back = models.FileField(upload_to='Political/User/adhaar_cards/', null=True, blank=True)
    pan_card_no = models.CharField(max_length=10, null=True, blank=True)
    pan_card_pic_front = models.FileField(upload_to='Political/User/pan_cards/', null=True, blank=True)
    pan_card_pic_back = models.FileField(upload_to='Political/User/pan_cards/', null=True, blank=True)
    voter_id_no = models.CharField(max_length=20, null=True, blank=True)
    voter_id_pic_front = models.FileField(upload_to='Political/User/voter_id/', null=True, blank=True)
    voter_id_pic_back = models.FileField(upload_to='Political/User/voter_id/', null=True, blank=True)

    present_door_no = models.CharField(max_length=32, null=True, blank=True)
    present_street = models.CharField(max_length=64, null=True, blank=True)
    present_locality_name = models.CharField(max_length=64, null=True, blank=True)
    present_landmark_name = models.CharField(max_length=64, null=True, blank=True)
    present_city = models.CharField(max_length=64, null=True, blank=True)
    present_state = models.CharField(max_length=64, null=True, blank=True)
    present_pincode = models.CharField(max_length=32, null=True, blank=True)
    present_country = models.CharField(max_length=64, null=True, blank=True)
    alternate_mobile = models.BigIntegerField(null=True, blank=True)
    father_name = models.CharField(max_length=64, null=True, blank=True)
    mothers_name = models.CharField(max_length=64, null=True, blank=True)
    medical_issue = models.CharField(max_length=512, null=True, blank=True)
    ACCOUNT_STATUS = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'))
    account_status = models.CharField(default='Active', max_length=16, choices=ACCOUNT_STATUS)
    REGISTRATION_STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Terminated', 'Terminated'))
    registration_status = models.CharField(default='Pending', max_length=32, choices=REGISTRATION_STATUS)
    MARITAL_STATUS = (
        ('Married', 'Married'),
        ('Unmarried', 'Unmarried'))
    marital_status = models.CharField(default='Unmarried', max_length=32, choices=MARITAL_STATUS, null=True, blank=True)
    added_datetime = models.DateTimeField(null=True, blank=True)
    updated_datetime = models.DateTimeField(null=True, blank=True)


class Employee_Login(models.Model):
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee_uuid = models.OneToOneField(Employee, on_delete=models.CASCADE)
    password = models.CharField(max_length=40)
    lastLogin = models.DateTimeField(null=True, blank=True)
    lastPasswordUpdated = models.DateTimeField(null=True, blank=True)

class Employee_Otp(models.Model):
    mobile_number = models.ForeignKey(Employee, on_delete=models.CASCADE)
    mobile_otp = models.CharField(max_length=10)