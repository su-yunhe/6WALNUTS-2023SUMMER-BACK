
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from file_manage.models import *

@csrf_exempt
def file_add(request):
    if request.method == "POST":
        filename = request.POST.get("fileName")
        fileinclude=request.POST.get("fileInclude")
        workid=request.POST.get("workId")
        groupid=request.POST.get("groupId")
        is_root=request.POST.get("is_root")
        print(is_root)
        new_file = Files()
        new_file.fileName = filename
        new_file.fileInclude = fileinclude
        new_file.fileIs_id=workid
        if is_root=='0':
            folderid=request.POST.get("folderId")
            print(1)
            new_file.folderIs=folderid
        else:
            new_file.folderIs=0
        new_file.save()
        fileurl=request.POST.get("fileUrl")+'/'+str(new_file.fileId)
        new_file.fileUrl = fileurl
        new_file.save()

        new_file_bro = File_Vers()
        new_file_bro.fileName = filename
        new_file_bro.fileInclude = fileinclude
        new_file_bro.fileIs_id=workid
        new_file_bro.fileId=new_file.fileId
        new_file_bro.fileVersion=1
        new_file_bro.folderIs=new_file.folderIs
        new_file_bro.save()
        fileurl=request.POST.get("fileUrl")+'/'+str(new_file_bro.fileId)
        new_file_bro.fileUrl = fileurl
        new_file_bro.save()

        groups=GroupUsers.objects.filter(groupId=groupid)
        print(list(groups.values()))
        for obj in groups:
            new_sample=File_Users()
            print(new_file.fileId)
            new_sample.fileId_id=new_file.fileId
            print(obj.userId.userId)
            new_sample.userId_id=obj.userId.userId
            new_sample.save()

        return JsonResponse({"error": 0, "msg": "新建文档成功"})
    else:
        return JsonResponse({"error": 2001, "msg": "请求方式错误"})

@csrf_exempt
def filemodel_add(request):
    if request.method == "POST":
        filename = request.POST.get("fileName")
        fileinclude=request.POST.get("fileInclude")
        fileid=request.POST.get("fileId")
        new_file = File_model()
        new_file.fileName = filename
        new_file.fileInclude = fileinclude
        new_file.fileId=fileid
        new_file.save()
        return JsonResponse({"error": 0, "msg": "新建模板文档成功"})
    else:
        return JsonResponse({"error": 2001, "msg": "请求方式错误"})

@csrf_exempt
def get_all_file(request):
    if request.method == "GET":
        results=list(Files.objects.all().values())
        if not results:  # 如果查询结果为空
            return JsonResponse({"error": 1001, "msg": "没有文档"})
       
        return JsonResponse({"error": 0, "msg": "获取所有文档成功","results": results})
    else:
        return JsonResponse({"error": 2001, "msg": "请求方式错误"})

@csrf_exempt
def file_modify_include(request):
    if request.method == "POST":
        fileinclude = request.POST.get("fileInclude")
        fileid = request.POST.get("fileId")
        results=Files.objects.get(fileId=fileid)
        results.fileInclude=fileinclude
        results.save()

        file_bro=File_Vers()
        file_bro.fileId=fileid
        file_bro.fileInclude=fileinclude
        file_bro.fileName=results.fileName+"("+str(((File_Vers.objects.filter(fileId=file_bro.fileId).last()).fileVersion)+1)+")"
        file_bro.fileUrl=results.fileUrl
        file_bro.fileIs_id=results.fileIs_id
        file_bro.fileVersion=((File_Vers.objects.filter(fileId=file_bro.fileId).last()).fileVersion)+1
        file_bro.save()
        return JsonResponse({"error": 0, "msg": "修改文档内容成功"})
    else:
        return JsonResponse({"error": 2001, "msg": "请求方式错误"})
    
@csrf_exempt
def file_delete(request):
    if request.method == "POST":
        fileid = request.POST.get("fileId")
        results=Files.objects.get(fileId=fileid)
        results.delete()
        return JsonResponse({"error": 0, "msg": "删除文档成功"})
    else:
        return JsonResponse({"error": 2001, "msg": "请求方式错误"})   
    
@csrf_exempt
def get_single_file(request):
    if request.method == "POST":
        fileid = request.POST.get("fileId")
        # print(fileid)
        results=list(Files.objects.filter(fileId=fileid).values())
        return JsonResponse({"error": 0, "msg": "获取文档成功","results": results})
    else:
        return JsonResponse({"error": 2001, "msg": "请求方式错误"})

@csrf_exempt
def get_model_file(request):
    if request.method == "POST":
        results=list(File_model.objects.values())
        return JsonResponse({"error": 0, "msg": "获取模板文档成功","results": results})
    else:
        return JsonResponse({"error": 2001, "msg": "请求方式错误"})

@csrf_exempt
def get_work_file(request):
    if request.method == "POST":
        workid = request.POST.get("workId")
        results=list(Files.objects.filter(fileIs_id=workid).values())
        print(results)
        return JsonResponse({"error": 0, "msg": "获取该项目的所有文档成功","results": results})
    else:
        return JsonResponse({"error": 2001, "msg": "请求方式错误"})

@csrf_exempt
def reference_check(request):
    if request.method == "POST":
       
        fileid = request.POST.get("fileId")
        user_now_id=request.POST.get("user_now_id")
        obj=File_Users.objects.filter(fileId_id=fileid).filter(userId_id=user_now_id)
        if not obj:
            return JsonResponse({"error": 1001, "msg": "没有该文档的修改权限"})
        return JsonResponse({"error": 0, "msg": "拥有权限"})
    else:
        return JsonResponse({"error": 2001, "msg": "请求方式错误"})
    
@csrf_exempt
def reference_add(request):
    if request.method == "POST":
       
        fileid = request.POST.get("fileId")
        user_now_id=request.POST.get("user_now_id")
        obj=File_Users()
        obj.fileId_id=fileid
        obj.userId_id=user_now_id
        obj.save()
        return JsonResponse({"error": 0, "msg": "新增用户权限成功"})
    else:
        return JsonResponse({"error": 2001, "msg": "请求方式错误"})
    
@csrf_exempt
def reference_delete(request):
    if request.method == "POST":
       
        fileid = request.POST.get("fileId")
        user_now_id=request.POST.get("user_now_id")
        obj=File_Users.objects.filter(fileId_id=fileid).filter(userId_id=user_now_id)
        if not obj:
            return JsonResponse({"error": 1001, "msg": "不存在对应的权限关系"})
        obj.delete()
        return JsonResponse({"error": 0, "msg": "删除用户权限成功"})
    else:
        return JsonResponse({"error": 2001, "msg": "请求方式错误"})
    
@csrf_exempt
def get_file_all_version(request):
    if request.method == "POST":
        fileid = request.POST.get("fileId")
        results=list(File_Vers.objects.filter(fileId=fileid).values())
        print(results)
        return JsonResponse({"error": 0, "msg": "获取所有文档版本成功","results": results})
    else:
        return JsonResponse({"error": 2001, "msg": "请求方式错误"})
    
@csrf_exempt
def file_version_back(request):
    if request.method == "POST":
        fileid = request.POST.get("fileId")
        fileversion=request.POST.get("fileVersion")
        target=File_Vers.objects.filter(fileId=fileid).filter(fileVersion=fileversion).get()
        origin=Files.objects.get(fileId=fileid)
        origin.fileInclude=target.fileInclude
        origin.save()
        return JsonResponse({"error": 0, "msg": "版本回退成功"})
    else:
        return JsonResponse({"error": 2001, "msg": "请求方式错误"})
    
@csrf_exempt
def message_relate(request):
    if request.method == "POST":
        fileid = request.POST.get("fileId")
        sendid=request.POST.get("sendId")
        receivename=request.POST.get("receiveName")
        new_file_message=File_Message()
        new_file_message.sendId_id=sendid
        new_file_message.receiveId_id=UserInfo.objects.get(userName=receivename).userId
        new_file_message.messageIs_id=fileid
        new_file_message.save()
        return JsonResponse({"error": 0, "msg": "@用户成功"})
    else:
        return JsonResponse({"error": 2001, "msg": "请求方式错误"})
    
@csrf_exempt
def check_file_message(request):
    if request.method == "POST":
        userid=request.POST.get("userId")
        results=File_Message.objects.filter(receiveId_id=userid).values()
        for obj in results:
            print(obj)
            obj['userName'] = UserInfo.objects.get(userId=obj['sendId_id']).userName
            obj['fileName'] = Files.objects.get(fileId=obj['messageIs_id']).fileName
            print(results)
        results = list(results)
        return JsonResponse({"error": 0, "msg": "获取所有@成功","results":results})
    else:
        return JsonResponse({"error": 2001, "msg": "请求方式错误"})

@csrf_exempt
def check_sender_name(request):
    if request.method == "POST":
        sendid=request.POST.get("sendId")
        results=list(UserInfo.objects.filter(userId=sendid).values('userName'))
        return JsonResponse({"error": 0, "msg": "获取发@人姓名成功","results":results})
    else:
        return JsonResponse({"error": 2001, "msg": "请求方式错误"})

@csrf_exempt
def add_folder(request):
    if request.method == "POST":
        folder_name=request.POST.get("folder_name")
        workid=request.POST.get("workId")
        new_folder=Folders()
        new_folder.folderName=folder_name
        new_folder.file_is_work=workid
        new_folder.save()
        return JsonResponse({"error": 0, "msg": "新建文件夹成功"})
    else:
        return JsonResponse({"error": 2001, "msg": "请求方式错误"})

@csrf_exempt
def get_file_tree(request):
    if request.method == "POST":
        workid=request.POST.get("workId")
        root_files=list(Files.objects.filter(folderIs='0').filter(fileIs_id=workid).values())
        root_folders=list(Folders.objects.filter(file_is_work=workid).values())
        son_files=list(Files.objects.filter().exclude(folderIs='0').filter(fileIs_id=workid).values())
        
        return JsonResponse({"error": 0, "msg": "获取成功","root_files":root_files,"root_folders":root_folders,"son_files":son_files})
    else:
        return JsonResponse({"error": 2001, "msg": "请求方式错误"})