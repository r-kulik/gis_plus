from django.shortcuts import render # type: ignore
from django.http import HttpResponse, HttpRequest, JsonResponse # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore
import os
import random
from faker import Faker
from django.utils import timezone
from .models import Companies, Fields, Wells, CurveMetrics, Files
from django.db.models import Q, Count


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
                well=random.choice(wells),
                internalStoragePath = fake.file_path(depth=3, category='text')
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

def exportFiles(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        file_filter = request.GET.get('fileFilter', None)
        field_filter = request.GET.get('fieldFilter', None)
        well_number_filter = request.GET.get('wellNumberFilter', None)
        start_measure_from_depth_filter = request.GET.get('startMeasureFromDepthFilter', None)
        finish_measure_from_depth_filter = request.GET.get('finishMeasureFromDepthDepthFilter', None)
        start_measure_till_depth_filter = request.GET.get('startMeasureTillDepthDepthFilter', None)
        finish_measure_till_depth_filter = request.GET.get('finishMeasureTillDepthDepthFilter', None)
        companies_filter = request.GET.get('companiesFilter', None)
        metrics_filter = request.GET.get('metricsFilter', )
        start_year_filter = request.GET.get('startYearFilter', None)
        finish_year_filter = request.GET.get('finishYearFilter', None)

        def convert_to_number(value, conversion_func):
            if value is None:
                return None
            try:
                return conversion_func(value)
            except ValueError:
                return None

        start_measure_from_depth_filter = convert_to_number(start_measure_from_depth_filter, float)
        finish_measure_from_depth_filter = convert_to_number(finish_measure_from_depth_filter, float)
        start_measure_till_depth_filter = convert_to_number(start_measure_till_depth_filter, float)
        finish_measure_till_depth_filter = convert_to_number(finish_measure_till_depth_filter, float)

        # Convert year filters to int if they are not None
        start_year_filter = convert_to_number(start_year_filter, int)
        finish_year_filter = convert_to_number(finish_year_filter, int)


        query = Q()

        # TODO: Сделать так, чтобы файлы и прочие хитрости, как и метрики можно было вводить через запятую
        if file_filter:
            query &= Q(filePath__icontains=file_filter)
        if field_filter:
            query &= Q(well__field__fieldName__icontains=field_filter)
        if well_number_filter:
            query &= Q(well__wellNumber__icontains=well_number_filter)

        if start_measure_from_depth_filter is not None:
            if finish_measure_from_depth_filter is not None:
                query &= Q(startDepth__range=(start_measure_from_depth_filter, finish_measure_from_depth_filter))
            else:
                query &= Q(startDepth__gte=start_measure_from_depth_filter)
        elif finish_measure_from_depth_filter is not None:
            query &= Q(startDepth__lte=finish_measure_from_depth_filter)

        if start_measure_till_depth_filter is not None:
            if finish_measure_till_depth_filter is not None:
                query &= Q(stopDepth__range=(start_measure_till_depth_filter, finish_measure_till_depth_filter))
            else:
                query &= Q(stopDepth__gte=start_measure_till_depth_filter)
        elif finish_measure_till_depth_filter is not None:
            query &= Q(stopDepth__lte=finish_measure_till_depth_filter)

        if companies_filter:
            query &= Q(company__companyName__icontains=companies_filter)
    

        
        
        if start_year_filter is not None and finish_year_filter is not None:
            query &= Q(datetime__year__range=(start_year_filter, finish_year_filter))
        elif start_year_filter is not None:
            query &= Q(datetime__year__gte=start_year_filter)
        elif finish_year_filter is not None:
            query &= Q(datetime__year__lte=finish_year_filter)
        print(query)
        
        files = Files.objects.select_related('company', 'well__field').filter(query).distinct()
        # files = Files.objects.select_related('company', 'well__field').prefetch_related('metrics')

        
        if metrics_filter:
            metrics_list = [metric.strip() for metric in metrics_filter.split(',') if metric.strip()]
    
            if metrics_list:
                metrics_query = Q()
                for metric in metrics_list:
                    metrics_query |= Q(metrics__metricName__iexact=metric)
        
                # Annotate the files with a count of matching metrics
                files = Files.objects.annotate(
                    matching_metrics_count=Count('metrics', filter=metrics_query)
                )
        
                # Filter files to ensure they have all specified metrics
                files = files.filter(matching_metrics_count=len(metrics_list))

                # Combine with the main query
                query &= Q(fileId__in=files.values_list('fileId', flat=True))
            
        files = files.prefetch_related('metrics').filter(query).distinct()
        file_list = []
        for file in files:
            file_data = {
                'fileId': file.fileId,
                'filePath': file.filePath,
                'fileVersion': file.fileVersion,
                'startDepth': file.startDepth,
                'stopDepth': file.stopDepth,
                'datetime': file.datetime,
                'companyName': file.company.companyName,
                'wellNumber': file.well.wellNumber,
                'fieldName': file.well.field.fieldName,
                'metrics': [metric.metricName for metric in file.metrics.all()],
                'internalStoragePath': file.internalStoragePath
            }
            file_list.append(file_data)

    return JsonResponse({'files': file_list})


        


    

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