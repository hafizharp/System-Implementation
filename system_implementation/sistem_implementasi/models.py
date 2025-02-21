from django.db import models

class SistemCerdas(models.Model):
    file_sistem_cerdas = models.FileField(upload_to='sistem_cerdas/')
    
    def __str__(self):
        return self.file_sistem_cerdas.name