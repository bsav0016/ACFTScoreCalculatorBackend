from rest_framework import serializers
from .models import ACFTResult, User, PaymentSheet


class ACFTResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ACFTResult
        fields = ('id', 'month', 'day', 'year', 'gender', 'age', 'deadlift_raw', 'deadlift_score', 'spt_raw',
                  'spt_score', 'pushups_raw', 'pushups_score', 'sdc_raw', 'sdc_score', 'plank_raw', 'plank_score',
                  'tmr_raw', 'tmr_score', 'total_score', 'user')



class UserSerializer(serializers.ModelSerializer):
    acft_results = ACFTResultSerializer(many=True, required=False)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'staff', 'admin', 'acft_results',
                  'paid_fee')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        #acft_results_data = validated_data.pop('acft_results')
        #acft_results = []
        #for acft_result in acft_results_data:
        #    acft_results.append(ACFTResult.objects.create(**acft_result))
        user = User.objects.update_user(**validated_data)#, acft_results=acft_results)
        return user

class PaymentSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentSheet
        fields = ('id', 'payment_intent', 'ephemeral_key', 'customer', 'publishable_key')
        extra_kwargs = {'payment_intent': {'write_only': True, 'required': True},
                        'ephemeral_key': {'write_only': True, 'required': True}}
