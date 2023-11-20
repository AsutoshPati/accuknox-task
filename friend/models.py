from django.db import models
from public.models import User


class FriendStack(models.Model):
    fid = models.AutoField(primary_key=True, editable=False, help_text='Friend ID')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_user_set', help_text='Friend request sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_user_set', help_text='Friend request receiver')
    status = models.CharField(max_length=1, choices=(('A', 'Accepted'), ('R', 'Rejected'), ('C', 'Canceled'), ('P', 'Pending')), default='P')
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    last_updated_at = models.DateTimeField(editable=False, auto_now=True)
