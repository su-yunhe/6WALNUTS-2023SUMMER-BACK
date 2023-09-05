from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from group_manage.models import Group, GroupUsers
from message.models import TeamMessage, Chat, ChatUser
from user_info.models import UserInfo


# 给群聊id返群聊名
@csrf_exempt
def getGroupName(request):
    if request.method == 'POST':
        groupid = request.POST.get('groupid')
        groupname = Group.objects.get(groupId=groupid).groupName
        return JsonResponse({'error': 0, 'msg': '请求方式错误', 'data': {'GroupName': groupname}})
    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


# 创建团队----->同时创建了公开群聊
@csrf_exempt
def buildGroup(request):
    if request.method == 'POST':
        groupname = request.POST.get('groupname')
        builder = request.POST.get('buildername')
        new_group = Group()
        new_group.groupName = groupname
        new_group.groupBuilder = builder
        new_group.save()

        groupid = new_group.groupId
        userid = request.POST.get('userid')
        usertype = 1  # 1表示创建者

        groupuser = GroupUsers()
        groupuser.groupId_id = groupid
        groupuser.userId_id = userid
        groupuser.userType = usertype
        groupuser.save()
        # 新增
        new_chat = Chat()
        new_chat.groupId_id = groupid
        new_chat.chatType = 1  # 公开群聊类型
        new_chat.save()
        new_chat.chatName = groupname

        chatuser = ChatUser()
        chatuser.chatId_id = new_chat.chatId
        chatuser.userId_id = userid
        chatuser.save()

        return JsonResponse({'error': 0, 'msg': '建立团队成功!', 'data': {'groupid': groupid}})
    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


# 管理员邀请他人加入团队
@csrf_exempt
def addUser(request):
    if request.method == 'POST':
        adminid = request.POST.get('adminid')
        groupid = request.POST.get('groupid')
        username = request.POST.get('userName')
        userid = UserInfo.objects.get(userName=username).userId
        if not TeamMessage.objects.filter(groupId=groupid, inviteId=userid).exists():
            team_message = TeamMessage()
            team_message.groupId_id = groupid
            team_message.adminId = adminid
            team_message.inviteId = userid
            team_message.save()
            return JsonResponse({'error': 0, 'msg': '邀请成功'})
        else:
            return JsonResponse({'error': 3001, 'msg': '已经邀请过了捏'})
    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


# 管理员踢出组员----->组员所在团队里的所有群聊也都被踢除
@csrf_exempt
def deleteUser(request):
    if request.method == 'POST':
        adminid = request.POST.get('adminid')
        groupid = request.POST.get('groupid')
        admin = GroupUsers.objects.get(userId=adminid, groupId=groupid)
        if admin.userType == 1 or admin.userType == 2:
            username = request.POST.get('userName')
            try:
                userid = UserInfo.objects.get(userName=username).userId
            except:
                return JsonResponse({'error': 4001, 'msg': '该用户不存在'})

            user = GroupUsers.objects.get(userId=userid, groupId=groupid)
            user.delete()
            # 所有群聊里的该组员删除，所有与该组员的私聊删除
            chat_id = Chat.objects.filter(groupId=groupid).values('chatId', 'chatType')
            for obj in chat_id:
                if obj['chatType'] == 3 and ChatUser.objects.filter(chatId=obj['chatId']).exists():
                    ChatUser.objects.filter(chatId=obj['chatId']).delete()
                    Chat.objects.filter(chatId=obj['chatId']).delete()
                if obj['chatType'] != 3:
                    ChatUser.objects.filter(chatId=obj['chatId'], userId=userid).delete()

            return JsonResponse({'error': 0, 'msg': '删除成员成功'})

        else:
            return JsonResponse({'error': 3001, 'msg': '您没有这个权限'})
    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


# 添加管理员
@csrf_exempt
def addAdmin(request):
    if request.method == 'POST':
        adminid = request.POST.get('adminid')
        groupid = request.POST.get('groupid')
        admin = GroupUsers.objects.get(userId=adminid, groupId=groupid)
        if admin.userType == 1:
            username = request.POST.get('userName')
            try:
                userid = UserInfo.objects.get(userName=username).userId
                user = GroupUsers.objects.get(userId=userid, groupId=groupid)
            except:
                return JsonResponse({'error': 4001, 'msg': '该用户不存在'})

            if user.userType == 3:
                user.userType = 2
                user.save()
                return JsonResponse({'error': 0, 'msg': '添加管理员成功'})

            else:
                return JsonResponse({'error': 4002, 'msg': '已经为管理员'})
        else:
            return JsonResponse({'error': 3001, 'msg': '您没有这个权限'})
    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


# 删除管理员
@csrf_exempt
def cancelAdmin(request):
    if request.method == 'POST':
        adminid = request.POST.get('adminid')
        groupid = request.POST.get('groupid')
        admin = GroupUsers.objects.get(userId=adminid, groupId=groupid)
        if admin.userType == 1:
            username = request.POST.get('userName')
            try:
                userid = UserInfo.objects.get(userName=username).userId
                user = GroupUsers.objects.get(userId=userid, groupId=groupid)
            except:
                return JsonResponse({'error': 4001, 'msg': '该用户不存在'})

            if user.userType == 2:
                user.userType = 3
                user.save()
                return JsonResponse({'error': 0, 'msg': '撤销管理员成功'})

            else:
                return JsonResponse({'error': 4002, 'msg': '他还不是管理员'})
        else:
            return JsonResponse({'error': 3001, 'msg': '您没有这个权限'})
    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


# 获取用户所有的所在团队
@csrf_exempt
def getAllGroup(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        group_users = GroupUsers.objects.filter(userId=userid)
        group = []
        if group_users.exists():
            for obj in group_users:
                groupid = obj.groupId.groupId
                group += list(Group.objects.filter(groupId=groupid).values())

            return JsonResponse({'error': 0, 'msg': '获取成功', 'data': group})
        else:
            return JsonResponse({'error': 3001, 'msg': '请先创建团队'})

    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


# 获取团队详细信息
@csrf_exempt
def getGroupInf(request):
    if request.method == 'POST':
        groupid = request.POST.get('groupid')
        group_users = GroupUsers.objects.filter(groupId=groupid)
        userinf = []
        for obj in group_users:
            userid = obj.userId.userId
            usertype = obj.userType
            listinf = list(UserInfo.objects.filter(userId=userid).values('userName', 'userEmail', 'userRealName'))
            listinf[0]['userType'] = usertype
            userinf += listinf
        return JsonResponse({'error': 0, 'msg': '获取成功', 'data': userinf})

    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


# 获得当前用户的身份权限
@csrf_exempt
def getType(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        groupid = request.POST.get('groupid')
        type = GroupUsers.objects.get(groupId=groupid, userId=userid).userType
        return JsonResponse({'error': 0, 'msg': '获取成功', 'data': {'userType': type}})

    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})
