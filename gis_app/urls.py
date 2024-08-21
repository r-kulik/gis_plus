from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
    path('import/', views.import_view, name='Импорт LAS-файлов'),
    path('upload/', views.upload_file, name='upload'),
    path('export/', views.export_view, name='Экспорт LAS-файлов'),
    path('exportFiles/', views.exportFiles, name='Возврат файлов по запросу'),
    path('save_to_database/', views.save_to_database, name='Сохранение файлов в базу'),
    path('downloadFiles/', views.downloadFiles, name='Download Files'),
]