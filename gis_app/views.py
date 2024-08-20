from django.shortcuts import render # type: ignore
from django.http import HttpResponse, HttpRequest, JsonResponse # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore
import os


def hello_world(request):
    return HttpResponse("Hello, World!")


def import_view(request: HttpRequest) -> HttpResponse:
    return render(
        request, 'import.html'
    )

@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES.getlist('files'):
        files = request.FILES.getlist('files')
        file_data = []
        for file in files:
            # Save file temporarily or process it
            file_path = os.path.join('temp_files', file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            file_data.append({
                'name': file.name,
                'size': file.size,
                'type': file.content_type,
                'path': file_path
            })
        return JsonResponse({'files': file_data})
    return JsonResponse({'error': 'No files uploaded'}, status=400)