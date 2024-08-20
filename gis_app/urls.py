from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
    path('import/', views.import_view, name='Импорт LAS-файлов'),
    path('upload/', views.upload_file, name='upload')
]