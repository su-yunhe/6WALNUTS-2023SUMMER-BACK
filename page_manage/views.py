from django.http import JsonResponse
from page_manage.models import *
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def page_add(request):
    if request.method == "POST":
        protoname = request.POST.get("protoName")
        workis = request.POST.get("workIs")
        protoinclude= request.POST.get("protoInclude")
        print(protoinclude)
        print(workis)
        print(protoname)
        new_proto = Prototypes()
        new_proto.protoName = protoname
        new_proto.workIs = workis
        new_proto.protoInclude=protoinclude
        new_proto.save()
        return JsonResponse({"error": 0, "msg": "新建原型成功"})
    else:
        return JsonResponse({"error": 2001, "msg": "请求方式错误"})

@csrf_exempt
def page_get(request):
    if request.method == "POST":
        workid = request.POST.get("workId")
        results=list(Prototypes.objects.filter(workIs=workid).values())
        return JsonResponse({"error": 0, "msg": "获取原型成功","results":results})
    else:
        return JsonResponse({"error": 2001, "msg": "请求方式错误"})
    
@csrf_exempt
def change_page_vaild(request):
    if request.method == "POST":
        protoid = request.POST.get("protoId")
        target=Prototypes.objects.get(protoId=protoid)
        print(target.is_vaild)
        if target.is_vaild==0:
            target.is_vaild=1
            target.save()
        else:
            print(1)
            target.is_vaild=0
            target.save()
        return JsonResponse({"error": 0, "msg": "修改原型状态成功"})
    else:
        return JsonResponse({"error": 2001, "msg": "请求方式错误"})