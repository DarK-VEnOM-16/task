from django.contrib import admin
from django.urls import path
from . import views
app_name='job'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('task', views.TaskViewPaginated.as_view() , name='job_list'),
    path('task/<int:id>', views.TaskDetailView.as_view() , name='task_by_id'),
    path('delete/', views.delete , name='delete'),
    path('create/', views.create , name='create'),
    path('update/', views.update , name='update'),
    path('',views.base,name="home")
]
