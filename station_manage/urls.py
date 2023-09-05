from django.urls import path
from .views import *


urlpatterns = [
    path("addwork", work_add),
    path("get_work_deleted", get_work_deleted),
    path("get_all_work", get_all_work),
    path("work_modify_name", work_modify_name),
    path("work_modify_condition", work_modify_condition),
    path("work_search", work_search),
    path("work_modify_isdoing", work_modify_isdoing),
    path("get_single_work", get_single_work),
    path("work_copy", work_copy),
    ]
