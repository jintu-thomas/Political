from django.urls import re_path, include
from . import views


urlpatterns =[
    re_path(r'^add_departments$', views.adding_departments, name="adding_departments"),
    re_path(r'^get_departments$', views.getting_departments, name="adding_departments"),
    re_path(r'^updating_departments$', views.updating_departments, name="updating_departments"),
    re_path(r'^adding_roles$', views.adding_roles, name="adding_roles"),
    re_path(r'^getting_roles$', views.getting_roles, name="getting_roles"),
    re_path(r'^updating_roles$', views.updating_roles, name="updating_roles"),
]