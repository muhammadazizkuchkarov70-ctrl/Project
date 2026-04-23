from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserEditForm, ProfileEditForm

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserEditForm(instance=request.user, data=request.POST)
        p_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserEditForm(instance=request.user)
        p_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'profile.html', {'u_form': u_form, 'p_form': p_form})