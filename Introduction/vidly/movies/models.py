from django.db import models
from django.utils import timezone

# Application data
# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=255)
    
    # Overwrite the __str__ method
    def __str__(self):
        return str(self.name)

class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_year = models.IntegerField()
    number_in_stock = models.IntegerField()
    daily_rate = models.FloatField()

    # Relationship with Genre
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    # Use a reference to a method
    date_created = models.DateTimeField(default=timezone.now)
