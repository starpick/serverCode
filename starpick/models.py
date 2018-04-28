from django.db import models

# Create your models here.

class User(models.Model):
    def __str__(self):
        return self.user_name + " " + self.password
    user_name = models.CharField(max_length=200)
    password = models.CharField(max_length=20)
