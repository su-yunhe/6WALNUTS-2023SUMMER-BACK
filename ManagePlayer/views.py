from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Player


# Create your views here.

@csrf_exempt
def addplayer(request):
    if request.method == 'POST':
        playerName = request.POST.get('playerName')
        playerAge = request.POST.get('playerAge')
        playerHeight = request.POST.get('playerHeight')
        playerWeight = request.POST.get('playerWeight')
        playerPosition = request.POST.get('playerPosition')
        new_player = Player()
        new_player.playerName = playerName
        new_player.playerAge = playerAge
        new_player.playerHeight = playerHeight
        new_player.playerWeight = playerWeight
        new_player.playerPosition = playerPosition
        new_player.save()
        return JsonResponse({'error': 0, 'msg': '添加球员成功'})
    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})