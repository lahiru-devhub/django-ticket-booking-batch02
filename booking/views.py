from django.shortcuts import render

# Create your views here.

def home(request):
    
    # fruits = ["Apple", "Orange", "Mango"]
    fruits = []
    
    return render(request, "booking/home.html", {
        'fruits' : fruits
    })

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
    