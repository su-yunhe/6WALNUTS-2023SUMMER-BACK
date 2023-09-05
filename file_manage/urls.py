from django.urls import path
from .views import *


urlpatterns = [
    path("file_add", file_add),
    path("get_all_file", get_all_file),
    path("file_modify_include", file_modify_include),
    path("file_delete", file_delete),
    path("get_single_file", get_single_file),
    path("reference_check", reference_check),
    path("reference_add", reference_add),
    path("reference_delete", reference_delete),
    path("get_work_file", get_work_file),
    path("get_file_all_version", get_file_all_version),
    path("file_version_back", file_version_back),
    path("message_relate", message_relate),
    path("check_file_message", check_file_message),
    path("check_sender_name", check_sender_name),
    path("add_folder", add_folder),
    path("get_file_tree", get_file_tree),
    path("get_model_file", get_model_file),
    path("filemodel_add", filemodel_add),
    ]
