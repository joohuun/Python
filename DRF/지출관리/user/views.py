from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from user.serializers import UserSerializer, TokenObtainPairSerializer
from user.models import User as UserModel
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    # 회원가입
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# 로그인
class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    

class OnlyAuthenticatedUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # 회원 정보 조회
    def get(self, request):
        user = request.user
        if not user:
            return Response({"error": "접근 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(UserSerializer(request.user).data)

    # 회원 정보 수정 (pk=user.id)
    def put(self, request, pk):
        user = UserModel.objects.get(pk=pk)
        if request.user != user:
            return Response({"error": "접근 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        user_serializer = UserSerializer(user, request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        return Response(user_serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
    # 로그아웃   
    def delete(self, request):
        print(self.request)
        logout(request)
        print(request)
        return Response({"로그아웃 성공"})