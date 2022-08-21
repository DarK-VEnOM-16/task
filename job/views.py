from django.http import HttpResponse
from django.shortcuts import render,redirect,reverse
from .models  import Task
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)
from .serializer import TaskSerializer
from rest_framework.response import Response
from rest_framework import status
from .renderers import CustomApiRenderer
from rest_framework.pagination import PageNumberPagination
import requests
from django.conf import settings
# Create your views here.


class TaskViewPaginated(ListCreateAPIView):
    serializer_class = TaskSerializer
    model = Task
    limit = 1
    offset = 0
    # pagination_class=PageNumberPagination
    def get_queryset(self):
        print('Heiii')
        # dashmed_agent detects the device and its version
        q_offset = self.request.GET.get("offset", self.offset)
        q_query = self.request.GET.get("q", None)
        q_sort_expiry = self.request.GET.get("sortByExpiry", None)
        # decodin q_query url
        q_query_decoded = unquote(q_query) if q_query else None
        self.offset = int(q_offset)
        task_qs=self.model.objects.all()

        return task_qs

    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        if self.pagination_class is not None:
            res.data["limit"] = int(self.limit)
            res.data["offset"] = int(self.offset) + int(self.limit)
            data = res.data
        else:
            data = {"stockSize": 0, "taskList": res.data}
        response = {"status": True, "data": data}
        return Response(data=response, status=status.HTTP_200_OK)
    def create(self, request, *args, **kwargs):

        # cleaning contact number data

        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            response = {
                "data":serializer.errors,
                "message": "Task creation failed",
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


        created_obj = self.model.objects.create(
            **serializer.validated_data,
        )

        # sending notification on add to the new party
        response = {
            "message": "Task created successfully",
        }
        return Response(data=response, status=status.HTTP_201_CREATED)

class TaskDetailView(RetrieveUpdateDestroyAPIView):

    serializer_class = TaskSerializer
    model = Task
    lookup_url_kwarg = "id"
    renderer_classes = [CustomApiRenderer]

    def get_object(self):
        
        pk = self.kwargs.get("id")
        print("TTTy"*100,pk)
        try:
            obj = self.model.objects.get(id=pk)
            print(obj)
        except self.model.DoesNotExist:
            return None
        return obj

    def get(self, request, *args, **kwargs):
        res = super().get(request, *args, **kwargs)
        response = {
            "data": res.data,
            "message": "Retrieved successfully",
        }
        return Response(data=response, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        print('AAA'*100)
        if self.get_object() is None:
            return Response(
                data={"message": "Not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data =request.data
        # change category array into comma separated
        serializer = self.get_serializer(self.get_object(), data=data)
        if not serializer.is_valid():
            print(serializer.errors)
            response = {
                "data": str(serializer.errors),
                "message": str(serializer.errors),
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        response = {
            "message": "Task entry updated successfully",
        }
        return Response(data=response, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        if self.get_object() is None:
            return Response(
                data={"message": "Requested resource does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        res = super().delete(request, *args, **kwargs)
        response = {"message": "Task entry deleted successfully"}
        return Response(data=response, status=status.HTTP_200_OK)

def base (request):
    print(f"{settings.BASE_SITE_URL}{str(reverse('job:job_list'))}")
    response = requests.get(f"{settings.BASE_SITE_URL}{str(reverse('job:job_list'))}")
    print(response.json())
    context={
        "data" : response.json()['data']['taskList']
    }
    return render(request,'home.html',context)

def create(request):
    if request.method == 'POST':
        title=request.POST['title']
        description=request.POST['description']
        priority=request.POST['priority']
        start_on=request.POST['start_on']
        end_on=request.POST['end_on']
        try:
            if int(request.POST['id'] ) !=0:
                print('sadasdsadsadsadsadsadsaddas'*5)
                id=request.POST['id']
                data={
                    "title" :title,
                    "description":description,
                    "priority" :priority,
                    "start_on":start_on,
                    "end_on" :end_on
                }
                print(f"{settings.BASE_SITE_URL}/task/"+str(id))
                response = requests.put(f"{settings.BASE_SITE_URL}/task/"+str(id),data=data)

                print("try"*100)
                print(response)
                return redirect('job:home')
        except:
            data={
                "title" :title,
                "description":description,
                "priority" :priority,
                "start_on":start_on,
                "end_on" :end_on
            }
            print(f"{settings.BASE_SITE_URL}{str(reverse('job:job_list'))}")
            response = requests.post(f"{settings.BASE_SITE_URL}{str(reverse('job:job_list'))}",data=data)

            print("try"*100)
            print(response)
            return redirect('job:home')
    else:
        return render(request,'create_form.html')

def delete(request):
    if request.method == 'POST':
        id=request.POST['id']
        print(f"{settings.BASE_SITE_URL}/task/"+str(id))
        response = requests.delete(f"{settings.BASE_SITE_URL}/task/"+str(id))
        print(response)
        return redirect('job:home')
def update(request):
    if request.method == 'POST':
        id=request.POST['id']
        obj=Task.objects.get(id=int(id))
        context={
            "id":id,
            "title" :obj.title,
            "description":obj.description,
            "priority" :obj.priority,
            "start_on":obj.start_on,
            "end_on" :obj.end_on
        }
        return render(request,'create_form.html',context)
    else:

        pass

def read(request):
    pass