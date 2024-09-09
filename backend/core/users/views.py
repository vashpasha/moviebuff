from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serializers import UserSerializer, UserDataSerializer, UserEditSerializer, ChangePasswordSerializer
from .models import UserData


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LogOutView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'log out successfully'}, status=204)

class UserMeDetailView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = request.user
        serializer = UserDataSerializer(user)
        return Response(serializer.data)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, id):
        try:
            user = UserData.objects.get(id=id)
        except UserData.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserDataSerializer(user)
        return Response(serializer.data)

class UserListView(APIView):
    permission_classes = [IsAdminUser, ]

    def get(self, request):
        users = UserData.objects.all()
        serializer = UserDataSerializer(users, many=True)
        return Response(serializer.data)

class UserEditView(APIView):
    permission_classes = [IsAuthenticated, ]

    def put(self, request):
        user = request.user
        serializer = UserEditSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated, ]

    def put(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.update(user, serializer.validated_data)
            return Response({'detail': 'password change successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)