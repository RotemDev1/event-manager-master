from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .email import sendResetPasswordEmail, generateKey, timeIsValid
from .forms import UserRegisterForm, ResetPasswordForm, ResetPasswordEnterForm, EditProfileForm


# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Your account {username} has been created! Now you can log in')
            return redirect('login')

    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    args = {'user': request.user}
    return render(request, 'users/profile.html', args)


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(
                request, ' Your profile edit successfull')
            return redirect('edit_profile')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'users/edit_profile.html', args)



@login_required
@permission_required('is_superuser')
def users(request):
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    if limit is None:
        limit = 5
    else:
        limit = int(limit)
        if limit < 1 or limit > 20:
            limit = 5

    p = Paginator(User.objects.all(), limit)
    if page is None:
        page = 1
    else:
        page = int(page)
        if page < 1 or page > p.num_pages:
            page = 1
    context = {
        'page_obj': p.get_page(page)
    }
    return render(request, 'users/users_list.html', context)


def adminResetPassword(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            users = User.objects.filter(email=email)
            if len(users) > 0:
                if (users[0].is_superuser):
                    sendResetPasswordEmail(email)
                    messages.success(
                        request, f'Successfully sent email to {email} with instructions')
                    return redirect('login')
                else:
                    messages.warning(
                        request, f'Email {email} not found')
            else:
                messages.warning(
                    request, f'Email {email} not found')
    else:
        form = ResetPasswordForm()
    context = {
        'form': form
    }
    return render(request, 'admin/reset.html', context)


def adminResetPasswordEnter(request):
    expire = False
    bad_sign = False
    form = None
    if request.method == 'POST':
        u = request.GET.get('u')
        email = request.GET.get('email')
        key = request.GET.get('key')
        if u is None or email == None or key == None:
            bad_sign = True
        else:
            if timeIsValid(u):
                if generateKey(email, u) == key:
                    form = ResetPasswordEnterForm(request.POST)
                    if form.is_valid():
                        u = User.objects.get(email=email)
                        u.set_password(request.POST.get('password1'))
                        u.save()
                        messages.success(
                            request, 'Successfully changed password')
                        return redirect('login')
                else:
                    bad_sign = True
            else:
                expire = True
    else:
        u = request.GET.get('u')
        email = request.GET.get('email')
        key = request.GET.get('key')
        if u is None or email == None or key == None:
            bad_sign = True
        else:
            if timeIsValid(u):
                if generateKey(email, u) == key:
                    form = ResetPasswordEnterForm()
                else:
                    bad_sign = True
            else:
                expire = True
    context = {
        'form': form,
        'expire': expire,
        'bad_sign': bad_sign
    }
    return render(request, 'admin/reset_password_enter.html', context)
