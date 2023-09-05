from django.urls import path

from group_manage.views import *

urlpatterns = [
    path('buildGroup', buildGroup),
    path('addUser', addUser),
    path('deleteUser', deleteUser),
    path('addAdmin', addAdmin),
    path('cancelAdmin', cancelAdmin),
    path('getAllGroup', getAllGroup),
    path('getGroupInf', getGroupInf),
    path('getType', getType),
    path('getGroupName', getGroupName)
]