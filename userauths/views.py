from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate # [04:40]
from django.contrib import messages # [05:40]

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