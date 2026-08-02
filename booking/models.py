from django.db import models
import uuid
from django.core.validators import MinValueValidator

# Create your models here.

class Venue(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["name"]
        
    def __str__(self):
        return self.name
    
class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #1 ,2,3  550e8400-e29b-41d4-a716-446655440000
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT, related_name="events")
    title = models.CharField(max_length=255)
    description = models.TextField()
    event_date = models.DateField()
    event_time = models.TimeField()
    image = models.ImageField(upload_to="events/", blank=True,null=True)
    is_published = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(0)])
    available_tickets = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now_add=True) 
    
    
    class Meta:
        ordering = ["event_date", "event_time"]
        indexes = [
                models.Index(fields=["event_date", "is_published"]),
        ]
        
    def __str__(self):
        return self.title