from dotenv import load_dotenv
import os
import random
import time
import json
from django.shortcuts import render
from django.http import JsonResponse
from agora_token_builder import RtcTokenBuilder
from .models import RoomMember
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

load_dotenv()


def get_token(request):
    # app_id = os.getenv('APP_ID')
    # app_certificate = os.getenv('APP_CERTIFICATE')
    app_id = "bd46496e208e467fa3331f094c0689cf"
    app_certificate = "3924f3fdef5e4ff593bbc5af54dbefd8"
    channel_name = request.GET.get('channel')
    uid = random.randint(1, 230)
    expiration_time_in_seconds = 3600 * 24
    current_timestamp = time.time()
    privilege_expires_at = current_timestamp + expiration_time_in_seconds
    role = 1
    token = RtcTokenBuilder.buildTokenWithUid(app_id, app_certificate, channel_name, uid, role, privilege_expires_at)
    return JsonResponse({'token': token, 'uid': uid}, safe=False)


def lobby(request):
    return render(request, 'app/lobby.html')


def room(request):
    return render(request, 'app/room.html')


@csrf_exempt
def create_member(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    return JsonResponse({'name': data['name']}, safe=False)


def get_member(request):
    uid = request.GET.get('uid')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name
    )
    name = member.name
    return JsonResponse({'name': name}, safe=False)


@csrf_exempt
def delete_member(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member was deleted.', safe=False)