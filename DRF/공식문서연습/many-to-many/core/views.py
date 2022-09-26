# Create your views here.
from imp import new_module
from . models import Menu
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Students, Modules
from .serializers import StudentsSerializer, ModulesSerializer

@csrf_exempt
def menu(request):
    if request.method == 'GET':
        menu_list = Menu.objects.all()
        return JsonResponse({'data':f"{menu_list}"})
        
    
    if request.method == 'POST':
        menu_list = Menu(branch_code="스타벅스", name='아메리카노')
        menu_list.save()
        
        menu_list.option.add('1', '2')
        menu_list.save()
        
        return JsonResponse({'data':f"{menu_list}"})


class StudentsViewSet(viewsets.ModelViewSet):
    serializer_class = StudentsSerializer

    def get_queryset(self):
        student = Students.objects.all()
        return student

    def create(self, request, *args, **kwargs):
        data = request.data
        print(data, "36363636")
        
        # for new_student in data["name"]:
        #     new_student = Students.objects.filter(
        #         name=data["name"])
        #     return JsonResponse(data=data)
        
        
        new_student = Students.objects.all()
        new_student.save()          
    
        for module in data["modules"]:
            module_obj = Modules.objects.get(module_name=module["module_name"])
            new_student.modules.add(module_obj)

        serializer = StudentsSerializer(new_student)

        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        data = request.data

        new_student = Students.objects.create(
            name=data["name"], age=data['age'], grade=data["grade"])

        new_student.save()

        for module in data["modules"]:
            module_obj = Modules.objects.get(module_name=module["module_name"])
            new_student.modules.add(module_obj)

        serializer = StudentsSerializer(new_student)

        return Response(serializer.data)


class ModulesViewSet(viewsets.ModelViewSet):
    # queryset = Modules.objects.all()
    serializer_class = ModulesSerializer

    def get_queryset(self):
        module = Modules.objects.all()
        return module
    
    
    def create(self, request, *args, **kwargs):
        data = request.data
        print(data, "838383")

        new_module = Modules.objects.create(
            module_name=data["module_name"],
            module_duaration=data['module_duaration'],
            class_room=data["class_room"])

        new_module.save()
        
        

        for stu in data["students"]:
            print(data["students"], "94949494")
            stu_obj = Students.objects.get(name=stu["name"])
            new_module.modules.add(stu_obj)

        serializer = ModulesSerializer(new_module)

        return Response(serializer.data)
    