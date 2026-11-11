from django.db import models
from django.conf import settings

class Document(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True
    )
    
    title = models.CharField(max_length=200)
    document_type = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    notes = models.TextField(blank=True)
    

    def __str__(self):
        return self.title
