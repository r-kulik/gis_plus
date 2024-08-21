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
    fileId = models.AutoField(primary_key=True)
    filePath = models.FilePathField()
    fileVersion = models.CharField(max_length=5)
    startDepth = models.FloatField()
    stopDepth = models.FloatField()
    datetime = models.DateTimeField(null=True, blank=True)
    company = models.ForeignKey(to=Companies, on_delete=models.CASCADE)
    well = models.ForeignKey(to=Wells, on_delete=models.CASCADE)
    metrics = models.ManyToManyField(CurveMetrics)
    internalStoragePath = models.FilePathField()
    internalHash = models.CharField(max_length=64, unique=True)  # Assuming SHA-256 hash

    def save(self, *args, **kwargs):
        if not self.internalHash:
            # Calculate the hash of the file content
            file_path = os.path.join('temp_files', self.internalStoragePath.strip())
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                self.internalHash = file_hash
        super(Files, self).save(*args, **kwargs)