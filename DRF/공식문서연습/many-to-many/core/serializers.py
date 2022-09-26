from rest_framework import serializers
from .models import Modules, Students





class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = ['name']
        # fields = '__all__'
        # depth = 1
        
        
class ModulesSerializer(serializers.ModelSerializer):
    students = StudentsSerializer(many=True, source='modules')
    
      
    class Meta:
        model = Modules
        fields = ['module_name', 'students']
        # fields = '__all__'
