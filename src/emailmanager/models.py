from django.db import models

# Create your models here.




# EMAIL CLASS
class Emails(models.Model):
    sender = models.TextField()
    title = models.TextField()
    content = models.TextField() 