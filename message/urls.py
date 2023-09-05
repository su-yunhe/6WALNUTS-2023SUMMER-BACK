from django.urls import path

from message.views import *

urlpatterns = [
    path('message/reference/queryAll', getCenterMessage),
    path('message/reference/read', haveRead),
    path('message/reference/deleteAll', deleteAllHaveRead),
    path('message/reference/delete', deleteOneHaveRead),
    path('message/invitation/queryAll', getAllInviteTeam),
    path('message/invitation/answer', getAnswerTeam),
    path('message/groupChat/queryAll', getAllInviteChat),
    path('message/groupChat/answer', getAnswerChat),
    path('message/chat/dissolution', dissolutionMessage),
    path('message/chat/queryAll', getAllDissolutionMessage),
    path('team/detail/inviteMembers', inviteChat),
    path('team/detail/createChat', createChat),
    path('team/detail/requestChatList', getChatList),
    path('team/detail/jumpToPrivateChat', getChatid),
    path('team/detail/dissolutionChat', dissolutionChat),
    path('team/detail/requestHistory', getAllMessage),
    path('team/detail/requestMembers', getChatMember),
    path('team/detail/quitChat', quitChat),
    path('message/groupChat/confirm', getConfirm)
]
