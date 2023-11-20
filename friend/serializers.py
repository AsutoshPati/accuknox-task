from rest_framework import serializers

from .models import *


class FriendRequestSerializer(serializers.Serializer):
    receiver = serializers.IntegerField()

    def validate(self, data):
        errors = dict()

        if hasattr(self, 'initial_data'):
            unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())
            if unknown_keys:
                for i in unknown_keys:
                    errors.update({i: ["Got unknown field"]})
                raise serializers.ValidationError({"errors": errors})

        if 'receiver' in data:
            if not User.objects.filter(uid=data['receiver'], is_active=True).first():
                errors.update({'receiver': ["User doesn't exist"]})

        if errors:
            raise serializers.ValidationError({"errors": errors})

        return data


class FriendStackSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendStack
        fields = '__all__'

    def validate(self, data):
        errors = dict()

        if hasattr(self, 'initial_data'):
            unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())
            if unknown_keys:
                for i in unknown_keys:
                    errors.update({i: ["Got unknown field"]})
                raise serializers.ValidationError({"errors": errors})

        print(data)

        if errors:
            raise serializers.ValidationError({"errors": errors})

        return data


class FriendStatusSerializer(serializers.Serializer):
    fid = serializers.IntegerField()
    status = serializers.ChoiceField(choices=(('A', 'Accepted'), ('R', 'Rejected'), ('C', 'Canceled'), ('P', 'Pending')))

    def validate(self, data):
        errors = dict()

        if hasattr(self, 'initial_data'):
            unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())
            if unknown_keys:
                for i in unknown_keys:
                    errors.update({i: ["Got unknown field"]})
                raise serializers.ValidationError({"errors": errors})

        if 'fid' in data:
            if not FriendStack.objects.filter(fid=data['fid']).first():
                errors.update({'fid': ["Friend request doesn't exist"]})

        if 'status' in data:
            if data['status'] == 'P':
                errors.update({'fid': ["Friend request can't be updated to 'Pending'"]})

        if errors:
            raise serializers.ValidationError({"errors": errors})

        return data
