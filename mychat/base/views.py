from django.shortcuts import render
from django.http import JsonResponse
import random
import time
from agora_token_builder import RtcTokenBuilder
from .models import RoomMember
import json
from django.views.decorators.csrf import csrf_exempt



# Create your views here.

def lobby(request):
    return render(request, 'base/lobby.html')

def room(request):
    return render(request, 'base/chatroom.html')


def getToken(request):
    appId = ""
    appCertificate = ""
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600 * 24
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token,'uid': uid}, safe=False)


# def getToken(request):
#     appId = "963d8c32e9b64f57917feba588872c5a"
#     appCertificate = "cfb615492f8b47fbb752f9fea508a390"
#     channelName = request.GET.get('channel')
    
#     if not channelName:
#         return JsonResponse({'error': 'Channel name is required'}, status=400)
    
#     uid = int(request.GET.get('uid', random.randint(1, 999999)))
#     expirationTimeInSeconds = int(request.GET.get('expiry', 3600))
#     currentTimeStamp = int(time.time())
#     privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
#     role = 1  # Set role (1 for publisher)

#     try:
#         token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
#         return JsonResponse({'token': token, 'uid': uid})
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name':data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

# @csrf_exempt
# def deleteMember(request):
#     data = json.loads(request.body)
#     try:
#         member = RoomMember.objects.get(
#             name=data['name'],
#             uid=data['UID'],
#             room_name=data['room_name']
#         )
#         member.delete()
#         return JsonResponse('Member deleted', safe=False)
#     except RoomMember.DoesNotExist:
#         return JsonResponse({'error': 'Member does not exist'}, status=404)

@csrf_exempt
def deleteMember(request):
    try:
        data = json.loads(request.body)
        print("Delete request data:", data)
        member = RoomMember.objects.get(
            name=data['name'],
            uid=data['UID'],
            room_name=data['room_name']
        )
        member.delete()
        return JsonResponse('Member deleted', safe=False)
    except RoomMember.DoesNotExist:
        return JsonResponse({'error': 'Member does not exist'}, status=404)
    except Exception as e:
        print("Error in delete_member:", str(e))
        return JsonResponse({'error': str(e)}, status=500)

