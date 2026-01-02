from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate 
from django.contrib import messages 

def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save() #Saves the user
            
            #Get data for messages and login
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}!") 
            
            # Auto-Login Logic
            # Note: We don't need to manually authenticate here because we just created the user object.
            # We can just log them in directly with the backend.
            login(request, new_user) 
            
            return redirect('core:index') # Redirect to homepage
            
    else:
        form = UserRegisterForm()

    context = {
        'form': form
    }
    return render(request, 'userauths/signup.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:index')  

    if request.method == "POST":
        email = request.POST.get('email')  
        password = request.POST.get('password')

    
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('core:index')
        else:
          
            messages.error(request, "Invalid email or password.")

    return render(request, 'userauths/sign-in.html')