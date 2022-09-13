from django.shortcuts import render
from rest_framework import viewsets
from django.apps import apps
from rest_framework.response import Response
from rest_framework.decorators import action
# Create your views here.


from safedelete.models import HARD_DELETE

class SoftDeleteViewSet(viewsets.ViewSet):

    @action(detail=False)
    def deletes(self, request):
        queryset_id_list = apps.get_model('staffs', self.basename).objects.deleted_only().values_list('id', flat=True)
        return Response(queryset_id_list)

    @action(detail=True, methods = ['patch', 'delete'])
    def dodelete(self, request, pk):
        queryset = apps.get_model('staffs', self.basename).objects.deleted_only().get(id=pk)
        if self.request.method == "PATCH":
            queryset.undelete()\
                
            queryset.save()
        elif self.request.method == "DELETE":
            queryset.delete(force_policy=HARD_DELETE)
            queryset.save()
        return Response(f'{self.request.method} successful')