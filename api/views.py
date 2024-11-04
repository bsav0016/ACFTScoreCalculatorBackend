from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import ACFTResult
from .serializers import ACFTResultSerializer, UserSerializer
from django.contrib.auth import get_user_model

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class CustomObtainAuthToken(ObtainAuthToken):
    permission_classes = (AllowAny,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    authentication_classes = (TokenAuthentication, )


class ACFTResultViewSet(viewsets.ModelViewSet):
    queryset = ACFTResult.objects.all()
    serializer_class = ACFTResultSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    @action(detail=True, methods=['POST'])
    def save_results(self, request, pk=None):
        data = request.data
        data = data['data']

        print(data)

        month = int(data['month'])
        day = int(data['day'])
        year = int(data['year'])
        gender = str(data['gender'])
        age = int(data['age'])
        deadlift_raw = int(data['deadlift_raw'])
        deadlift_score = int(data['deadlift_score'])
        pushups_raw = int(data['pushups_raw'])
        pushups_score = int(data['pushups_score'])
        spt_raw = float(data['spt_raw'])
        spt_score = int(data['spt_score'])
        sdc_raw = int(data['sdc_raw'])
        sdc_score = int(data['sdc_score'])
        plank_raw = int(data['plank_raw'])
        plank_score = int(data['plank_score'])
        tmr_raw = int(data['tmr_raw'])
        tmr_score = int(data['tmr_score'])
        total_score = int(data['total_score'])

        user = request.user

        try:
            new_acft_result = ACFTResult.objects.create(month=month,
                                    day=day,
                                    year=year,
                                    gender=gender,
                                    age=age,
                                    deadlift_raw=deadlift_raw,
                                    deadlift_score=deadlift_score,
                                    spt_raw=spt_raw,
                                    spt_score=spt_score,
                                    pushups_raw=pushups_raw,
                                    pushups_score=pushups_score,
                                    sdc_raw=sdc_raw,
                                    sdc_score=sdc_score,
                                    plank_raw=plank_raw,
                                    plank_score=plank_score,
                                    tmr_raw=tmr_raw,
                                    tmr_score=tmr_score,
                                    total_score=total_score,
                                    user=user)
            serializer = ACFTResultSerializer(new_acft_result, many=False)
            response = {'message': 'Stored ACFT score', 'request': serializer.data}
            ACFTResult.save(new_acft_result)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {'message': "Sorry, this didn't work"}
            print(e)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        response = {'message': 'You can not update request like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {'message': 'You can not create request like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
