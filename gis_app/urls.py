from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
    path('import/', views.import_view, name='Импорт LAS-файлов'),
    path('upload/', views.upload_file, name='upload'),
    path('export/', views.export_view, name='Экспорт LAS-файлов'),
    path('exportFiles/', views.exportFiles, name='Возврат файлов по запросу'),
    path('save_to_database/', views.save_to_database, name='Сохранение файлов в базу'),
    path('downloadFiles/', views.downloadFiles, name='Download Files'),
    path('get_image_url/', views.get_image_url, name='get_image_url'),
    path('get_internal_storage_path/', views.get_internal_storage_path, name='get_internal_storage_path'),
    path('get_file_text_by_name/', views.get_file_text_by_name, name='get_file_text_by_name'),
    path('get_file_text_by_id/', views.get_file_text_by_id, name='get_file_text_by_id'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)