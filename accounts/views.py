from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def login_view(request):
    
    form = LoginForm(request.POST or None)
    next_url =  request.POST.get('next') or  request.GET.get('next')  or 'dashboard' #/login/?next=/booking
    
    if request.method == "POST":
        if form.is_valid():
            identifier = form.cleaned_data["identifier"].strip() # " dsqdqd "
            password = form.cleaned_data["password"]
            
            username = identifier
            
            user_model = get_user_model()
            
            matching_user = user_model.objects.filter(email__iexact = identifier).only("username").first()
            
            if matching_user is not None:
                username = matching_user.get_username()
                
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect(next_url)
            
            form.add_error(None, "Invalid username/email or password")
            
    return render(request, "accounts/login.html", {"form": form, "next" : next_url})


def register_view(request):
    
    if request.method == "POST":
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            
            user = form.save()
            login(request, user)
            return redirect("dashboard")
        
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {'form' : form})

def logout_view(request):
    logout(request)
    return redirect("home")

@login_required
def dashboard_view(request):
        
    return render(request, "accounts/dashboard.html")