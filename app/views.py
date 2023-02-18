from dotenv import load_dotenv
import os
import random
import time
from django.shortcuts import render
from django.http import JsonResponse
from agora_token_builder import RtcTokenBuilder
# Create your views here.

load_dotenv()


def get_token(request):
    app_id = os.getenv('APP_ID')
    app_certificate = os.getenv('APP_CERTIFICATE')
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
