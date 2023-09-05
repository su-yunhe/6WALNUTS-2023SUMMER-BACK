from distutils.util import strtobool

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from group_manage.models import GroupUsers, Group
from message.models import Message, UserMessage, TeamMessage, Chat, ChatUser, ChatMessage
from user_info.models import UserInfo


# 获取当前团队的某个群聊里所有成员id和昵称
@csrf_exempt
def getChatMember(request):
    if request.method == 'POST':
        chatid = request.POST.get('chatid')
        chatuser = ChatUser.objects.filter(chatId=chatid).values('userId')
        user = []
        for obj in chatuser:
            user += list(UserInfo.objects.filter(userId=obj['userId']).values('userId', 'userName'))
        return JsonResponse({'error': 0, 'msg': '获取成功', 'data': user})

    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


# 获取当前团队的某个群聊里所有消息
@csrf_exempt
def getAllMessage(request):
    if request.method == 'POST':
        chatid = request.POST.get('chatid')
        messageinf = list(Message.objects.filter(chatId=chatid).values('senderName', 'time', 'content', 'messageId'))
        for obj in messageinf:
            username = obj['senderName']
            userid = UserInfo.objects.get(userName=username).userId
            obj['userId'] = userid

        return JsonResponse({'error': 0, 'msg': '获取成功', 'data': messageinf})

    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


# 将未读改为已读
@csrf_exempt
def haveRead(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        messageid = request.POST.get('messageid')
        usermessage = UserMessage.objects.get(targetId=userid, messageId=messageid)
        if not usermessage.state:
            usermessage.state = True
            usermessage.save()
            return JsonResponse({'error': 0, 'msg': '已读成功'})
        else:
            return JsonResponse({'error': 3001, 'msg': '消息已经读过了'})

    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


# 删除消息中心所有已读消息
@csrf_exempt
def deleteAllHaveRead(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        usermessage = UserMessage.objects.filter(targetId=userid)
        for obj in usermessage:
            if obj.state:
                obj.delete()

        return JsonResponse({'error': 0, 'msg': '一键删除成功'})

    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


# 删除指定消息
@csrf_exempt
def deleteOneHaveRead(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        messageid = request.POST.get('messageid')
        usermessage = UserMessage.objects.filter(targetId=userid, messageId=messageid)
        usermessage.delete()

        return JsonResponse({'error': 0, 'msg': '删除该条消息成功'})

    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


# 消息中心获取所有被@的提示消息
@csrf_exempt
def getCenterMessage(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        usermessage = UserMessage.objects.filter(targetId=userid)
        new_message = []
        if usermessage.exists():
            for obj in usermessage:
                state = obj.state
                messageid = obj.messageId.messageId
                chatId = obj.messageId.chatId.chatId
                chatname = obj.messageId.chatId.chatName
                message = list(
                    Message.objects.filter(messageId=messageid).values('messageId', 'content', 'time', 'senderName'))
                message[0]['state'] = state
                message[0]['chatName'] = chatname
                message[0]['chatId'] = chatId
                new_message += message

            return JsonResponse({'error': 0, 'msg': '获取成功', 'data': new_message})

        else:
            return JsonResponse({'error': 3001, 'msg': '暂无消息'})

    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


# 消息中心获取所有邀请加入团队的消息
@csrf_exempt
def getAllInviteTeam(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        if TeamMessage.objects.filter(inviteId=userid).exists():
            invitation = list(TeamMessage.objects.filter(inviteId=userid).values('id', 'adminId', 'groupId'))
            for obj in invitation:
                groupname = Group.objects.get(groupId=obj['groupId']).groupName
                username = UserInfo.objects.get(userId=obj['adminId']).userName
                obj['groupName'] = groupname
                obj['userName'] = username

            return JsonResponse({'error': 0, 'msg': '获取成功', 'data': invitation})

        else:
            return JsonResponse({'error': 0, 'msg': '暂无通知'})

    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


# 消息中心获取所有邀请加入某群聊的消息
@csrf_exempt
def getAllInviteChat(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        if ChatMessage.objects.filter(inviteId=userid, type=1).exists():
            invitation = list(ChatMessage.objects.filter(inviteId=userid, type=1).values('id', 'adminId', 'chatId'))
            for obj in invitation:
                chatname = Chat.objects.get(chatId=obj['chatId']).chatName
                username = UserInfo.objects.get(userId=obj['adminId']).userName
                obj['chatName'] = chatname
                obj['userName'] = username
            return JsonResponse({'error': 0, 'msg': '获取成功', 'data': invitation})

        else:
            return JsonResponse({'error': 0, 'msg': '暂无通知', 'data': []})

    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


# 消息中心获取所有群聊被解散的消息
@csrf_exempt
def getAllDissolutionMessage(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        if ChatMessage.objects.filter(inviteId=userid, type=2).exists():
            chatmessage = list(ChatMessage.objects.filter(inviteId=userid, type=2).values('id', 'chatName'))
            return JsonResponse({'error': 0, 'msg': '暂无通知', 'data': chatmessage})

        else:
            return JsonResponse({'error': 0, 'msg': '暂无通知', 'data': []})

    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


# 加入某团队（可以拒绝），若接受，自动加入团队的公聊以及自动创建此人与团队所有人的私聊
@csrf_exempt
def getAnswerTeam(request):
    if request.method == 'POST':
        _id = request.POST.get('id')
        option = strtobool(request.POST.get('option'))
        if option:
            # 加入团队
            userid = TeamMessage.objects.get(id=_id).inviteId
            groupid = TeamMessage.objects.get(id=_id).groupId_id

            new_groupuser = GroupUsers()
            new_groupuser.groupId_id = groupid
            new_groupuser.userId_id = userid
            new_groupuser.userType = 3
            new_groupuser.save()

            # 加入公共群聊
            chatid = Chat.objects.get(groupId=groupid, chatType=1).chatId
            new_chatuser = ChatUser()
            new_chatuser.chatId_id = chatid
            new_chatuser.userId_id = userid
            new_chatuser.save()

            # 和团队里所有人建立私聊
            users = list(GroupUsers.objects.filter(groupId=groupid).values('userId'))
            for obj in users:
                if userid != obj['userId']:
                    username1 = UserInfo.objects.get(userId=userid).userName
                    username2 = UserInfo.objects.get(userId=obj['userId']).userName
                    new_chat = Chat()
                    new_chat.chatType = 3
                    new_chat.chatName = username1+'和'+username2+'的私聊'
                    new_chat.groupId_id = groupid
                    new_chat.save()
                    id1 = new_chat.chatId
                    chatuser1 = ChatUser()
                    chatuser1.chatId_id = id1
                    chatuser1.userId_id = userid
                    chatuser1.save()
                    chatuser2 = ChatUser()
                    chatuser2.chatId_id = id1
                    chatuser2.userId_id = obj['userId']
                    chatuser2.save()

        # 无论接受还是拒接，删除该条消息
        team_message = TeamMessage.objects.filter(id=_id)
        team_message.delete()
        return JsonResponse({'error': 0, 'msg': '操作成功'})
    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


# 加入某群聊（可以拒绝）
@csrf_exempt
def getAnswerChat(request):
    if request.method == 'POST':
        _id = request.POST.get('id')
        option = strtobool(request.POST.get('option'))
        if option:
            # 加入群聊
            userid = ChatMessage.objects.get(id=_id).inviteId
            chatid = ChatMessage.objects.get(id=_id).chatId
            if not ChatUser.objects.filter(chatId=chatid, userId=userid).exists():
                new_chatuser = ChatUser()
                new_chatuser.chatId_id = chatid
                new_chatuser.userId_id = userid
                new_chatuser.save()

        # 无论接受还是拒接，删除该条消息
        chat_message = ChatMessage.objects.filter(id=_id)
        chat_message.delete()
        return JsonResponse({'error': 0, 'msg': '操作成功'})
    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


# 创建群聊
@csrf_exempt
def createChat(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        groupid = request.POST.get('groupid')
        chatname = request.POST.get('chatname')

        new_chat = Chat()
        new_chat.chatType = 2
        new_chat.leaderId = userid
        new_chat.chatName = chatname
        new_chat.groupId_id = groupid
        new_chat.save()

        chatid = new_chat.chatId
        new_chatuser = ChatUser()
        new_chatuser.chatId_id = chatid
        new_chatuser.userId_id = userid
        new_chatuser.save()

        return JsonResponse({'error': 0, 'msg': '创建成功', 'data': {'chatId': chatid}})
    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


# 邀请某些人加入群聊
@csrf_exempt
def inviteChat(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        inviteid = request.POST.get('inviteid')
        chatid = request.POST.get('chatid')
        chatname = Chat.objects.get(chatId=chatid).chatName

        new_chatmessage = ChatMessage()
        new_chatmessage.chatId = chatid
        new_chatmessage.adminId = userid
        new_chatmessage.inviteId = inviteid
        new_chatmessage.chatName = chatname
        new_chatmessage.type = 1
        new_chatmessage.save()

        return JsonResponse({'error': 0, 'msg': '邀请成功'})

    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


# 群主解散多人群聊
@csrf_exempt
def dissolutionChat(request):
    if request.method == 'POST':
        chatid = request.POST.get('chatid')
        chat = Chat.objects.filter(chatId=chatid)
        chat.delete()
        chatuser = ChatUser.objects.filter(chatId=chatid)
        chatuser.delete()
        return JsonResponse({'error': 0, 'msg': '解散群聊'})

    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


# 消息中心增加群聊被解散的消息
@csrf_exempt
def dissolutionMessage(request):
    if request.method == 'POST':
        chatname = request.POST.get('chatname')
        chatid = request.POST.get('chatid')
        userid = request.POST.get('userid')
        new_chatmessage = ChatMessage()
        new_chatmessage.type = 2
        new_chatmessage.chatId = chatid
        new_chatmessage.chatName = chatname
        new_chatmessage.adminId = 0
        new_chatmessage.inviteId = userid
        new_chatmessage.save()

        return JsonResponse({'error': 0, 'msg': '解散群聊成功'})

    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


# 获取当前用户当前团队的所有群聊
@csrf_exempt
def getChatList(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        chatuser = ChatUser.objects.filter(userId=userid).values('chatId')
        chat = []
        for obj in chatuser:
            chat += list(Chat.objects.filter(chatId=obj['chatId']).values())

        return JsonResponse({'error': 0, 'msg': '获取成功', 'data': chat})

    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


# 在某个多人聊天里选择和某人私聊
@csrf_exempt
def getChatid(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        inviteid = request.POST.get('inviteid')
        chatuser1 = ChatUser.objects.filter(userId=userid).values('chatId')
        chatuser2 = ChatUser.objects.filter(userId=inviteid).values('chatId')
        chatid = []
        for user1 in chatuser1:
            for user2 in chatuser2:
                if user2['chatId'] == user1['chatId'] and Chat.objects.get(chatId=user1['chatId']).chatType == 3:
                    chatid = user1['chatId']
                    break

        return JsonResponse({'error': 0, 'msg': '获取成功', 'data': {'chatId': chatid}})

    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


# 退出群聊
@csrf_exempt
def quitChat(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        chatid = request.POST.get('chatid')
        chatuser = ChatUser.objects.get(chatId=chatid, userId=userid)
        chatuser.delete()
        return JsonResponse({'error': 0, 'msg': '退出群聊成功'})
    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


# 删除消息中心中的某条被解散的消息
@csrf_exempt
def getConfirm(request):
    if request.method == 'POST':
        _id = request.POST.get('id')
        chatmessage = ChatMessage.objects.filter(id=_id)
        chatmessage.delete()
        return JsonResponse({'error': 0, 'msg': '删除成功'})
    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})