
import random
import string

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from file_manage.models import *
from page_manage.models import *
from station_manage.models import *


@csrf_exempt
def work_add(request):
    if request.method == "POST":
        workname = request.POST.get("workName")
        groupid = request.POST.get("groupId")
        leader= request.POST.get("leader")
        introduction=request.POST.get("introduction")
        new_work = Works()
        new_work.workName = workname
        new_work.groupIs_id = groupid
        new_work.workCondition="进行中"
        new_work.workIntroduction=introduction
        new_work.leader=leader
        new_work.create_time=datetime.datetime.now().date()
        new_work.save()
        return JsonResponse({"error": 0, "msg": "建立项目成功"})
    else:
        return JsonResponse({"error": 2001, "msg": "请求方式错误"})

@csrf_exempt   
def get_work_deleted(request):
    if request.method == "GET":
        results=list(Works.objects.filter(isDelete=1).values())
        print(results)
        if not results:  # 如果查询结果为空
            return JsonResponse({"error": 1001, "msg": "没有找到被删除的项目"})
       
        return JsonResponse({"error": 0, "msg": "获取删除的项目成功","results": results})
    else:
        return JsonResponse({"error": 2001, "msg": "请求方式错误"})
    
@csrf_exempt
def get_all_work(request):
    if request.method == "POST":
        groupid=request.POST.get("groupId")
        print(groupid)
        results=list(Works.objects.filter(isDelete=0).filter(groupIs_id=groupid).order_by('-create_time','workName').values())
        
        #"workId","workName","isDelete","groupIs_id"
        print(results)
        if not results:  # 如果查询结果为空
            return JsonResponse({"error": 1001, "msg": "没有项目"})
       
        return JsonResponse({"error": 0, "msg": "获取所有项目成功","results": results})
                            
    else:
        return JsonResponse({"error": 2001, "msg": "请求方式错误"})
    
@csrf_exempt
def get_single_work(request):
    if request.method == "POST":
        workid = request.POST.get("workId")
        results=list(Works.objects.filter(workId=workid).values())
        if not results:  # 如果查询结果为空
            return JsonResponse({"error": 1001, "msg": "没有项目"})
       
        return JsonResponse({"error": 0, "msg": "获取项目成功","results": results})
    else:
        return JsonResponse({"error": 2001, "msg": "请求方式错误"})

@csrf_exempt
def work_modify_name(request):
    if request.method == "POST":
        print('-----------')
        workname = request.POST.get("workName")
        print(workname)
        print('-----------')
        workid = request.POST.get("workId")
        print(workid)
        results=Works.objects.get(workId=workid)
        results.workName=workname
        results.save()
        return JsonResponse({"error": 0, "msg": "修改项目名称成功"})
    else:
        return JsonResponse({"error": 2001, "msg": "请求方式错误"})
    
@csrf_exempt
def work_modify_condition(request):
    if request.method == "POST":
        isdelete = request.POST.get("isDelete")
        workid = request.POST.get("workId")
        results=Works.objects.get(workId=workid)
        results.isDelete=isdelete
        results.save()
        return JsonResponse({"error": 0, "msg": "修改项目状态成功"})
    else:
        return JsonResponse({"error": 2001, "msg": "请求方式错误"})

@csrf_exempt
def work_modify_isdoing(request):
    if request.method == "POST":
        workcondition = request.POST.get("workCondition")
        workid = request.POST.get("workId")
        results=Works.objects.get(workId=workid)
        results.workCondition=workcondition
        results.save()
        return JsonResponse({"error": 0, "msg": "修改项目进行状态成功"})
    else:
        return JsonResponse({"error": 2001, "msg": "请求方式错误"})

@csrf_exempt
def work_search(request):
    if request.method == "POST":
        workname = request.POST.get("workName")
        work_list=list(Works.objects.filter(workName__icontains=workname).values())
        if not work_list:
            return JsonResponse({"error": 1001, "msg": "没有找到符合条件的项目"})
        return JsonResponse({"error": 0, "msg": "查询成功","results":work_list})
    else:
        return JsonResponse({"error": 2001, "msg": "请求方式错误"})
    


@csrf_exempt
def work_copy(request):
    if request.method == "POST":
        s = string.ascii_letters
        r = random.choice(s)
        old_workid = request.POST.get("workId")
        origin_work=Works.objects.get(workId=old_workid)
        work_copy=Works()
        work_copy.workName=origin_work.workName+"(副本"+r+")"
        work_copy.isDelete=origin_work.isDelete
        work_copy.groupIs_id=origin_work.groupIs_id
        work_copy.create_time=origin_work.create_time
        work_copy.leader=origin_work.leader
        work_copy.workCondition=origin_work.workCondition
        work_copy.workIntroduction=origin_work.workIntroduction
        work_copy.save()
        new_work_id=work_copy.workId


        all_protoyes=Prototypes.objects.all()
        for obj in all_protoyes:
            if str(obj.workIs)==old_workid:
                prototype_copy=Prototypes()
                prototype_copy.protoInclude=obj.protoInclude
                prototype_copy.protoName=obj.protoName
                prototype_copy.workIs=work_copy.workId
                prototype_copy.is_vaild=obj.is_vaild
                prototype_copy.save()
        
        all_folders=Folders.objects.all()
        for obj in all_folders:
            if str(obj.file_is_work)==old_workid:
                folder_copy=Folders()
                folder_copy.folderName=obj.folderName
                folder_copy.file_is_work=work_copy.workId
                folder_copy.save()

                all_file_son_copy=Files.objects.filter(folderIs=obj.folderId)
                for o in all_file_son_copy:
                    file_son_copy=Files()
                    file_son_copy.fileName=o.fileName
                    file_son_copy.fileUrl=o.fileUrl
                    file_son_copy.fileInclude=o.fileInclude
                    file_son_copy.fileIs_id=work_copy.workId
                    file_son_copy.folderIs=folder_copy.folderId
                    file_son_copy.save()

                    all_file_users=File_Users.objects.all()
                    for i in all_file_users:
                        if i.fileId_id==o.fileId:
                            file_user_copy=File_Users()
                            file_user_copy.fileId_id=file_son_copy.fileId
                            file_user_copy.userId_id=i.userId_id
                            file_user_copy.save()

                    all_file_messages=File_Message.objects.all()
                    for j in all_file_messages:
                        if j.messageIs_id==o.fileId:
                            file_message_copy=File_Message()
                            file_message_copy.sendId_id=j.sendId_id
                            file_message_copy.receiveId_id=j.receiveId_id
                            file_message_copy.messageIs_id=file_son_copy.fileId
                            file_message_copy.save()

                    all_file_versions=File_Vers.objects.all()
                    for k in all_file_versions:
                        if k.fileId==o.fileId:
                            file_version_copy=File_Vers()
                            file_version_copy.fileId=file_son_copy.fileId
                            file_version_copy.fileName=k.fileName+"("+"副本"+")"
                            file_version_copy.fileInclude=k.fileInclude
                            file_version_copy.fileUrl=k.fileUrl
                            file_version_copy.fileInclude=k.fileInclude
                            file_version_copy.fileIs_id=work_copy.workId
                            file_version_copy.folderIs=k.folderIs
                            file_version_copy.save()


        all_files=Files.objects.filter(folderIs=0)
        for obj in all_files:
            if str(obj.fileIs_id)==old_workid:
                file_copy=Files()
                file_copy.fileName=obj.fileName
                file_copy.fileUrl=obj.fileUrl
                file_copy.fileInclude=obj.fileInclude
                file_copy.fileIs_id=work_copy.workId
                file_copy.folderIs=obj.folderIs
                file_copy.save()

                all_file_users=File_Users.objects.all()
                for i in all_file_users:
                    if i.fileId_id==obj.fileId:
                        file_user_copy=File_Users()
                        file_user_copy.fileId_id=file_copy.fileId
                        file_user_copy.userId_id=i.userId_id
                        file_user_copy.save()

                all_file_messages=File_Message.objects.all()
                for j in all_file_messages:
                    if j.messageIs_id==obj.fileId:
                        file_message_copy=File_Message()
                        file_message_copy.sendId_id=j.sendId_id
                        file_message_copy.receiveId_id=j.receiveId_id
                        file_message_copy.messageIs_id=file_copy.fileId
                        file_message_copy.save()

                all_file_versions=File_Vers.objects.all()
                for k in all_file_versions:
                    if k.fileId==obj.fileId:
                        file_version_copy=File_Vers()
                        file_version_copy.fileId=file_copy.fileId
                        file_version_copy.fileName=k.fileName+"("+"副本"+")"
                        file_version_copy.fileInclude=k.fileInclude
                        file_version_copy.fileUrl=k.fileUrl
                        file_version_copy.fileInclude=k.fileInclude
                        file_version_copy.fileIs_id=work_copy.workId
                        file_version_copy.folderIs=k.folderIs
                        file_version_copy.save()


                
                    
        return JsonResponse({"error": 0, "msg": "复制成功"})
    else:
        return JsonResponse({"error": 2001, "msg": "请求方式错误"})


