from django.shortcuts import redirect, render

def home(request):
    if not request.user.is_authenticated:
        return render(request, 'capstone/home.html')
    else:
        if request.user.is_person:
            return redirect('persons:event_list')
        else:
            return redirect('organisations:event_change_list')


def sign_up(request):
    return render(request, 'registration/signup.html')



