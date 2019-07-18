from django.shortcuts import redirect

def homepage(request):
    return redirect('accounts/login')