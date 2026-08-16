from django.shortcuts import render
from .models import Event
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from django.conf import settings

from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.core.mail import EmailMultiAlternatives

# Create your views here.

def home(request):

    latest_events = Event.objects.filter(is_published=True).select_related('venue')[:10]
    
    context = {
        "latest_events" : latest_events
    }
    
    return render(request, "booking/home.html", context)

def events_view(request):
    
    events = Event.objects.filter(is_published=True).select_related("venue")

    context = {
        "events" : events
    }    

    return render(request, "booking/events.html", context)

def event_detail_view(request, event_id):
    
    event = get_object_or_404(
        Event.objects.select_related("venue"),
        pk=event_id,
        is_published=True
    )
    
    context = {
        "event" : event
    }
    
    return render (
        request,
        "booking/event_detail.html",
        context
    )
    
@login_required
def book_event_view(request, event_id):
    
    event = get_object_or_404(
        Event.objects.select_related("venue"),
        pk=event_id,
        is_published=True
    )
    
    if request.method == "GET":
        
        context = {
            "event" : event,
            "quantity": 1,
            "quantity_options" : range(1, min(event.available_tickets, 5) + 1),
            "booking_total" : event.price
        }
        
        return render(request, "booking/book_event.html", context)
    
    
def _send_booking_confirmation(request, booking):
    if not booking.user.email:
        messages.warning(request, "Booking confirmed, but no email was sent because your account has no email address")
        return
    
    user_display_name = booking.user.get_full_name() or booking.user.username
    event = booking.event
    
    dashboard_url = request.build_absolute_uri(reverse("dashboard"))
    
    subject = f"Booking Confirmation - {event.title}"
    
    context ={
        "user_display_name" : user_display_name,
        "event" : event,
        "booking" : booking,
        "dashboard_url" : dashboard_url
    }
    
    html_message = render_to_string("booking/emails/booking_confirmation.html", context)
    text_message = strip_tags(html_message)
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[booking.user.email]
    )
    
    email.attach_alternative(html_message, "text/html")
    
    try:
        email.send(fail_silently=False)
    except Exception:
        messages.warning(
            request,
            "Booking confirmed, but confirmation email could not be sent. Please contact support.",
        )
    

def contact(request):
    
    context = {
        "user_data" :{
            "name": "Nimal",
            "email": "nimal@gmail.com"
        }
    }
    
    return render(request, "public/contact.html", context)

def about(request):
    return render(request, "public/about-us.html")

def faq(request):
    return render(request, "public/faq.html")
    
def custom_404(request, exception):
    return render(request, "404.html", status=404)