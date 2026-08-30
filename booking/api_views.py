from rest_framework import generics

from .serializer import VenueSerializer, EventSerializer
from .models import Event, Venue


class VenueListAPIView(generics.ListAPIView):
    # queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    
    def get_queryset(self):
        queryset = Venue.objects.all()
        
        name = self.request.query_params.get("name") #/api/venues/?name=test
        capacity = self.request.query_params.get("capacity")
        
        if name:
            queryset = queryset.filter(
                name__icontains= name
            )
            
        if capacity:
            queryset = queryset.filter(
                capacity__gte=capacity
            )
        
        return queryset
    
class EventListAPIView(generics.ListAPIView):
    
    serializer_class = EventSerializer
    
    def get_queryset(self):
        queryset = Event.objects.filter(is_published=True)
        
        title = self.request.query_params.get("title")
        venue_id  = self.request.query_params.get("venue")
        event_date  = self.request.query_params.get("date")
        
        if title:
            queryset = queryset.filter(
                title__icontains = title
            )
            
        if venue_id:
            queryset = queryset.filter(
                venue_id=venue_id
            )
            
        if event_date:
            queryset = queryset.filter(
                event_date=event_date
            )
            
        return queryset