from django.db import models

# Create your models here.




# EMAIL CLASS
class Email(models.Model):
    sender = models.CharField(max_length = 100)
    title = models.CharField(max_length = 100)
    content = models.TextField() 