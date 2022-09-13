from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status, permissions, viewsets
from .models import Expenditure, ExpenditureDetail
from .serializers import ExpenditureSerializer, ExpenditureDetailSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404
# Create your views here.


class ExpenditureView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    
    def get(self, request):
        user = request.user
        
        expenditures = Expenditure.objects.filter(Q(user=user, is_active=True)).order_by('-date')
        serializer = ExpenditureSerializer(expenditures, many=True)
        
        
        return Response(serializer.data, status=200)
    
    def post(self, request):
        request.data['user'] = request.user.id
        serializer = ExpenditureSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def put(self, request, pk):
        expenditure = Expenditure.objects.get(pk=pk)
        serializer = ExpenditureSerializer(expenditure, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    # 영구 삭제
    def delete(self, request, pk):
        user = request.user
        expenditures = get_object_or_404(Expenditure, pk=pk, user=user)
        expenditures.delete()
        return Response("삭제 완료!!")
    
    
# 소프트 삭제
class ExpenditureSoftDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    
    def patch(self, request, pk):
        expenditures = Expenditure.objects.get(pk=pk)
        if expenditures.is_active == False:
            expenditures.is_active = True
            expenditures.save()
            return Response("복구 완료!!")
        else:
            expenditures.is_active = False
            expenditures.save()
            return Response("소프트 삭제 완료!!")
    
    
class ExpenditureDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    
    def get(self, request, pk):
        details = ExpenditureDetail.objects.filter(expenditure=pk).order_by('-id')        
        serializer = ExpenditureDetailSerializer(details, many=True)
        return Response(serializer.data, status=200)
    
    def post(self, request, pk):
        user = request.user
        expenditure = Expenditure.objects.get(pk=pk)
        request.data['expenditure'] = expenditure.id
        request.data['user'] = user.id
        request.data['detail'] = request.data['detail']
        serializer = ExpenditureDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    
    def put(self, request, pk):
        user = request.user
        detail = ExpenditureDetail.objects.get(pk=pk)
        request.data['detail'] = request.data['detail']
        if detail.user == user:
            serializer = ExpenditureDetailSerializer(detail, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        return Response("수정 권한이 없습니다.", status=400)
    
    
    def delete(self, request, pk):
        user = request.user
        detail = ExpenditureDetail.objects.get(pk=pk)
        if detail.user == user:
            detail.delete()
            return Response("삭제 완료!!",status=200)
        return Response("삭제 권한이 없습니다.", status=400)
    
