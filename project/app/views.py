from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .serializers import StudentSerializer
from .models import Student
import io
import json
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def stulist(request):
    stu_list=Student.objects.all()
    print("Query_set=",stu_list)
    serilizer = StudentSerializer(stu_list,many=True)
    print("Serializer=",serilizer)
    print("python_data(serializer.data)=", serilizer.data)
    json_data =JSONRenderer().render(serilizer.data)
    print("json_data=",json_data)
    return HttpResponse(json_data,content_type='application/json' )

@csrf_exempt
def create(request):
    json_data=request.body
    stream = io.BytesIO(json_data)
    python_data=JSONParser().parse(stream)
    seriliazer = StudentSerializer(data = python_data)
    if seriliazer.is_valid():
        seriliazer.save()
        res = {'msg': 'Data Created'}
        json_data= JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json')
    json_data = JSONRenderer().render(seriliazer.errors)
    return HttpResponse(json_data, content_type='application/json')