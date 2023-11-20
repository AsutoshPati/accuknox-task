from datetime import timedelta
from django.db.models import Q
from django.utils import timezone
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from public.serializers import UserSerializer
from .models import *
from .serializers import *


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def list_users(request):
    if len(request.query_params) != 1 or 'search' not in request.query_params:
        return Response({'status': 400, 'message': "Only 'search' parameter should be provided"}, status=400)

    search_key = request.query_params['search'].strip().lower()
    if len(search_key) < 3:
        return Response({'status': 400, 'message': "Please provide atleast 3 characters"}, status=400)

    users = []
    searched_users = User.objects.filter(email=search_key).first()
    if searched_users:
        users.append({'uid': searched_users.uid, 'name': searched_users.name, 'gender': searched_users.gender,
                      'city': searched_users.city, 'state': searched_users.state, 'bio': searched_users.bio})
    else:
        searched_users = User.objects.filter(name__icontains=search_key).all()
        for user in searched_users:
            users.append(
                {'uid': user.uid, 'name': user.name, 'gender': user.gender, 'city': user.city, 'state': user.state,
                 'bio': user.bio})

    return Response({'status': 200, 'users': users}, status=200)


class FriendView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        auth_user = User.objects.filter(email=request.user.username).first()

        query = FriendStack.objects.filter(Q(sender=auth_user.uid) | Q(receiver=auth_user.uid))
        if request.query_params or 'filter' in request.query_params:
            if request.query_params['filter'] == 'A':
                query = query.filter(status='A')
            elif request.query_params['filter'] == 'P':
                query = query.filter(status='P')
        friend_details = query.all()
        response = []
        for detail in friend_details:
            response.append({'fid': detail.fid, 'sender': detail.sender.name, 'receiver': detail.receiver.name,
                             'status': detail.status, 'sent_time': detail.created_at})
        return Response({'status': 200, 'message': response}, status=200)

    def post(self, request):
        validated_data = FriendRequestSerializer(data=request.data)
        if not validated_data.is_valid(raise_exception=True):
            return Response({'status': 400, 'message': "Something went wrong"}, status=400)

        sender = User.objects.filter(email=request.user.username).first()
        receiver = User.objects.filter(uid=validated_data.data['receiver']).first()
        if sender.uid == receiver.uid:
            return Response({'status': 400, 'message': "Friend request can't be sent to self"}, status=400)

        one_minute_ago = timezone.now() + timedelta(minutes=-1)
        friend_requests = FriendStack.objects.filter(sender=sender.uid, created_at__gte=one_minute_ago).order_by('-created_at').all()
        if len(friend_requests) >= 3:
            return Response({'status': 400, 'message': "More than 3 friend requests can't be send in a minute"}, status=400)

        friend_detail = FriendStack.objects.filter(
            Q(sender=sender.uid, receiver=receiver.uid) | Q(sender=receiver.uid, receiver=sender.uid)).first()
        if friend_detail and friend_detail.status not in ['C', 'R']:
            return Response({'status': 400, 'message': {"request_status": friend_detail.status,
                                                        "message": "Existing friend data found"}}, status=400)

        friend_request = FriendStackSerializer(data={'sender': sender.uid, 'receiver': receiver.uid})
        if not friend_request.is_valid(raise_exception=True):
            return Response({'status': 400, 'message': "Something went wrong"}, status=400)

        friend_request.save()
        return Response({'status': 200, 'message': 'Friend request sent'}, status=200)

    def patch(self, request):
        auth_user = User.objects.filter(email=request.user.username).first()
        friend_data = FriendStatusSerializer(data=request.data)
        if not friend_data.is_valid(raise_exception=True):
            return Response({'status': 400, 'message': "Something went wrong"}, status=400)

        detail = FriendStack.objects.filter(fid=friend_data.data['fid']).first()
        if detail.status != 'P':
            return Response({'status': 400, 'message': "Only pending friend request can be updated"}, status=400)

        if detail.sender.uid == auth_user.uid and friend_data.data['status'] != 'C':
            return Response({'status': 400, 'message': "Sender can only cancel friend request"}, status=400)
        elif detail.receiver.uid == auth_user.uid and friend_data.data['status'] == 'C':
            return Response({'status': 400, 'message': "Receiver can only accept/reject friend request"}, status=400)

        friend_data.data.pop('fid')
        friend_request = FriendStackSerializer(detail, data=friend_data.data, partial=True)
        if not friend_request.is_valid(raise_exception=True):
            return Response({'status': 400, 'message': "Something went wrong"}, status=400)
        friend_request.save()
        detail = friend_request.data
        return Response({'status': 200, 'message': {'message': 'Friend request status updated'},
                         'response': {'fid': detail['fid'], 'sender': detail['sender'], 'receiver': detail['receiver'],
                                      'status': detail['status'], 'sent_time': detail['created_at']}}, status=200)
