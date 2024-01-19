from django.db import models

# Create your models here.
class Visitor(models.Model):
    user = models.CharField(max_length = 30)
    password = models.CharField(max_length = 20)
    name = models.CharField(max_length = 50)
    email = models.CharField(max_length = 30)
    vertified = models.BooleanField(default = False)

    class Meta:
        db_table = "visitor"

class Picture(models.Model):
    filename = models.CharField(max_length = 50)
    picture = models.ImageField(upload_to='static/pictures')

    class Meta:
        db_table = "picture"