from django.db import models

class Companies(models.Model):
    companyId = models.AutoField(primary_key=True)
    companyName = models.TextField()

class Fields(models.Model):  # Corrected from models.model to models.Model
    fieldId = models.AutoField(primary_key=True)
    fieldName = models.TextField()

class Wells(models.Model):
    wellId = models.AutoField(primary_key=True)
    wellNumber = models.TextField()
    field = models.ForeignKey(to=Fields, on_delete=models.CASCADE)

class CurveMetrics(models.Model):
    metricName = models.TextField()

class Files(models.Model):
    """
    Здесь и далее при описании моделей используется CamelNotation
    """
    fileId = models.AutoField(primary_key=True)
    filePath = models.FilePathField()
    fileVersion = models.CharField(max_length=5)
    startDepth = models.FloatField()
    stopDepth = models.FloatField()
    datetime = models.DateTimeField()
    company = models.ForeignKey(to=Companies, on_delete=models.CASCADE)
    well = models.ForeignKey(to=Wells, on_delete=models.CASCADE)
    metrics = models.ManyToManyField(CurveMetrics)
    internalStoragePath = models.FilePathField()