from django.db import models

class PointOfTable(models.Model):
    time = models.DateTimeField(blank=True, null=True)
    team_id = models.IntegerField()
    
