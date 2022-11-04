from django.contrib.auth import login, authenticate, logout
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from accounts.models import User
from accounts.serializers import UserRegisterSerializer, UserLoginSerializer, UserShortSerializer
from books_catalog.permissions import AnonymousOnly


class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AnonymousOnly,)
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserLoginView(GenericAPIView):
    queryset = User.objects.all()
    permission_classes = (AnonymousOnly,)
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        authenticate(request)
        return Response({'status': 'ok'})

    @action(detail=False, methods=['post'])
    def login(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class UserLogoutView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserShortSerializer

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'])
    def logout(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
