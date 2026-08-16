from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("events/", views.events_view, name="venue"),
    path("events/<uuid:event_id>/", views.event_detail_view, name="event_detail"),
    path("events/<uuid:event_id>/book", views.book_event_view, name="book_event"),
    path("contact", views.contact, name="contact"),
    path("about", views.about, name="about"),
    path("faq", views.faq, name="faq")
]
