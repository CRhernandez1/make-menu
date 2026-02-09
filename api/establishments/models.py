from django.db import models
import uuid

class Establishment(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField()
    address = models.TextField()
    phone = models.CharField(max_length=16)

class Table(models.Model):
    qr_code = models.TextField()
    # people = 

class Manage(models.Model):
    pass
    # role = 
    # start_date = 
    # end_date = 