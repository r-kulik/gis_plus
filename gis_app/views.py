import zipfile
from django.shortcuts import render # type: ignore
from django.http import HttpResponse, HttpRequest, JsonResponse # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore
import os
import random
from faker import Faker
from django.utils import timezone
from .models import Companies, Fields, Wells, CurveMetrics, Files
from django.db.models import Q, Count
import random
import string
from Las_handler.SuperLas import SuperLas
from django.forms.models import model_to_dict
import json


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


def import_view(request):
    return render(request, 'import.html', {'current_page': 'import'})

def export_view(request):
    return render(request, 'export.html', {'current_page': 'export'})

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
        metrics_filter = request.GET.get('metricsFilter', [])
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


def get_or_create_company(company_name):
    return Companies.objects.get_or_create(companyName=company_name)

# Function to get or create a Field
def get_or_create_field(field_name):
    return Fields.objects.get_or_create(fieldName=field_name)

# Function to get or create a Well
def get_or_create_well(well_number, field_name):
    field, _ = get_or_create_field(field_name)
    return Wells.objects.get_or_create(wellNumber=well_number, defaults={'field': field})

# Function to get or create a CurveMetric
def get_or_create_metric(metric_name):
    return CurveMetrics.objects.get_or_create(metricName=metric_name)
       
def file_entry_to_dict(file_entry):
    file_dict = model_to_dict(file_entry)
    file_dict['company'] = model_to_dict(file_entry.company)
    file_dict['well'] = model_to_dict(file_entry.well)
    file_dict['well']['field'] = model_to_dict(file_entry.well.field)
    file_dict['metrics'] = [model_to_dict(metric) for metric in file_entry.metrics.all()]
    return file_dict

    

@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES.getlist('files'):
        files = request.FILES.getlist('files')
        file_data = []
        for file in files:
            # Save file temporarily or process it
            def generate_random_string(length):
                characters = string.ascii_letters + string.digits  # Includes both letters (uppercase and lowercase) and digits
                random_string = ''.join(random.choice(characters) for _ in range(length))
                return random_string
            internalStoragePath = generate_random_string(48) + ".las"
            file_path = os.path.join('temp_files', internalStoragePath)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            # Magic check for LAS files
            processer = SuperLas()
            process_result = processer.process_file(internalStoragePath)

            processed_file_path = None
            features = process_result.get('features', {})
            company_name = features.get('company', None)
            well_number = features.get('well', None)
            metrics_list = features.get('mnemonic_list_rus', []) + features.get('mnemonic_list_eng', [])
            processed_file_path = features.get('file_path', None)
            file_version = features.get('version', None)
            start_depth = features.get('start_depth', None)
            stop_depth = features.get('stop_depth', None)
            datetime_value = features.get('datetime', None)
        
            file_data.append({
                    "status": process_result.get('status', 'error'),
                    'name': file.name,
                    'size': file.size,
                    'originalFilePath': internalStoragePath,
                    'processedFilePath': processed_file_path,
                    'description': process_result.get('description', 'No description'),
                    'company_name': company_name,
                    'well_number': well_number,
                    'metrics_list': metrics_list,
                    'file_version': file_version,
                    'start_depth': start_depth,
                    'stop_depth': stop_depth,
                    'datetime': datetime_value,
                    'errors': process_result.get('errors', [])
            }
            )
        return JsonResponse({'files': file_data})
    return JsonResponse({'error': 'No files uploaded'}, status=400)

@csrf_exempt
def save_to_database(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON data from the request body
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        for file_entry in data:
            company, _ = get_or_create_company(file_entry['company_name'])
            well, _ = get_or_create_well(file_entry['well_number'], field_name=file_entry['company_name'])
            metrics = [get_or_create_metric(metric_name)[0] for metric_name in file_entry['metrics_list']]
            

            print(file_entry['processedFilePath'])
            # костыль!
            if file_entry['datetime'] == '': file_entry['datetime'] = None
            file_entry_model = Files(
                filePath=file_entry['name'],
                fileVersion=file_entry['file_version'],
                startDepth=file_entry['start_depth'],
                stopDepth=file_entry['stop_depth'],
                datetime=file_entry['datetime'],
                company=company,
                well=well,
                internalStoragePath=file_entry['processedFilePath']
            )

            file_entry_model.save()
            file_entry_model.metrics.set(metrics)

        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def downloadFiles(request):
    if request.method == 'POST':
        print(request.POST)
        selected_files = request.POST.getlist('files[]')
        print(f"selected_files = {selected_files}")
        zip_filename = 'exported_files.zip'
        temp_zip = zipfile.ZipFile(zip_filename, 'w')
        name_counter = {}  # Dictionary to track file names and their counts

        for file_id in selected_files:
            try:
                file_obj = Files.objects.get(fileId=file_id)
                file_path = os.path.join('temp_files', (file_obj.internalStoragePath).strip())
                original_name = os.path.basename(file_obj.filePath)
                print(file_path)

                if os.path.exists(file_path):
                    # Handle name collisions
                    if original_name in name_counter:
                        name_counter[original_name] += 1
                        base, ext = os.path.splitext(original_name)
                        original_name = f"{base}_{name_counter[original_name]}{ext}"
                    else:
                        name_counter[original_name] = 0

                    temp_zip.write(file_path, original_name)
                else:
                    print(f"File not found: {file_path}")
            except Files.DoesNotExist:
                print(f"File with ID {file_id} does not exist")

        temp_zip.close()

        with open(zip_filename, 'rb') as zip_file:
            response = HttpResponse(zip_file.read(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename={zip_filename}'
            return response

    return HttpResponse('Invalid request', status=400)