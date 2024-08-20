from django.shortcuts import render # type: ignore
from django.http import HttpResponse, HttpRequest, JsonResponse # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore
import os
import random
import string
from datetime import datetime
from .models import Companies, Fields, Locations, CurveMetrics, Files


def hello_world(request):
    

    def random_string(length=10):
        return ''.join(random.choice(string.ascii_letters) for _ in range(length))

    def random_number(start=0, end=100):
        return random.uniform(start, end)

    def create_dummy_data():
        # Create dummy Companies
        company1 = Companies.objects.create(companyName=random_string())
        company2 = Companies.objects.create(companyName=random_string())

        # Create dummy Fields
        field1 = Fields.objects.create(fieldName=random_string())
        field2 = Fields.objects.create(fieldName=random_string())

        # Create dummy Locations
        location1 = Locations.objects.create(field=field1)
        location2 = Locations.objects.create(field=field2)

        # Create dummy CurveMetrics
        metric1 = CurveMetrics.objects.create(metricName=random_string())
        metric2 = CurveMetrics.objects.create(metricName=random_string())

        # Create dummy Files
        file1 = Files.objects.create(
            filePath=random_string(),
            fileVersion=random_string(5),
            startDepth=random_number(),
            stopDepth=random_number(),
            datetime=datetime.now(),
            company=company1,
            location=location1
        )
        file1.metrics.add(metric1, metric2)

        file2 = Files.objects.create(
            filePath=random_string(),
            fileVersion=random_string(5),
            startDepth=random_number(),
            stopDepth=random_number(),
            datetime=datetime.now(),
            company=company2,
            location=location2
        )
        file2.metrics.add(metric1)

    # Call the function to create dummy data
    create_dummy_data()
        
    return HttpResponse("Hello, World!")


def import_view(request: HttpRequest) -> HttpResponse:
    return render(
        request, 'import.html'
    )

@csrf_exempt
def upload_file(request):

    FileTOCheck = Files(

    )
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