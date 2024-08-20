from django.shortcuts import render # type: ignore
from django.http import HttpResponse, HttpRequest, JsonResponse # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore
import os
import random
from faker import Faker
from django.utils import timezone
from .models import Companies, Fields, Wells, CurveMetrics, Files


def hello_world(request):
    fake = Faker("ru_RU")

    def create_dummy_companies(num_companies=10):
        for _ in range(num_companies):
            Companies.objects.create(companyName=fake.company())

    def create_dummy_fields(num_fields=5):
        for _ in range(num_fields):
            Fields.objects.create(fieldName=fake.city())

    def create_dummy_wells(num_wells=20):
        fields = Fields.objects.all()
        for _ in range(num_wells):
            Wells.objects.create(wellNumber=fake.numerify(text='WELL-####'), field=random.choice(fields))

    def create_dummy_curve_metrics(num_metrics=10):
        for _ in range(num_metrics):
            CurveMetrics.objects.create(metricName=fake.job())

    def create_dummy_files(num_files=30):
        companies = Companies.objects.all()
        wells = Wells.objects.all()
        metrics = CurveMetrics.objects.all()
        for _ in range(num_files):
            file = Files.objects.create(
                filePath=fake.file_path(depth=3, category='text'),
                fileVersion=fake.numerify(text='v%#.##'),
                startDepth=random.uniform(100, 1000),
                stopDepth=random.uniform(1000, 5000),
                datetime=fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=timezone.get_current_timezone()),
                company=random.choice(companies),
                well=random.choice(wells)
            )
            file.metrics.set(random.sample(list(metrics), random.randint(1, 5)))

    def populate_database():
        create_dummy_companies()
        create_dummy_fields()
        create_dummy_wells()
        create_dummy_curve_metrics()
        create_dummy_files()
    populate_database()
    return HttpResponse("Hello, World!")


def import_view(request: HttpRequest) -> HttpResponse:
    return render(
        request, 'import.html'
    )

def export_view(request: HttpRequest) -> HttpResponse:
    return render(
        request, 'export.html'
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