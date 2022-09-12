from rest_framework import serializers
from .models import Expenditure, ExpenditureDetail, Category
from django.db.models import Sum


class CategorySerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Category
        field = "__all__"


class ExpenditureDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenditureDetail
        fields = "__all__"
        
        
class ExpenditureSerializer(serializers.ModelSerializer):
    detail = ExpenditureDetailSerializer(many=True, source="detail_set", read_only=True)
    total = serializers.SerializerMethodField()
    def get_total(self, obj):
        return Expenditure.objects.aggregate(Sum("amount"))
    
    class Meta:
        model = Expenditure
        fields = "__all__"