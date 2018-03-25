from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render

from members.forms import SignupForm

User = get_user_model()


__all__ = (
    'signup_view',
)


def signup_view(request):
    # context = {
    #     'errors': [],
    # }
    # if request.method == 'POST':
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     password2 = request.POST['password2']
    #
    #     is_valid = True
    #     if User.objects.filter(username=username).exists():
    #         context['errors'].append('Username already exists!')
    #         is_valid = False
    #     if password != password2:
    #         context['errors'].append('Password and Password2 are not equal!')
    #         is_valid = False
    #     if is_valid:
    #         User.objects.create_user(username=username, password=password)
    #         return redirect('index')
    # return render(request, 'members/signup.html', context)
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            is_valid = True
            # if User.objects.filter(username=username).exists():
            #     form.add_error('username', '이미 사용되고 있는 아이디입니다')
            #     is_valid = False
            # if password != password2:
            #     form.add_error('password2', '비밀번호 불일치')
            #     is_valid = False
            # if is_valid:
            User.objects.create_user(username=username, password=password)
            return redirect('index')
    else:
        form = SignupForm()

    context = {
        "signup_form": form,
    }
    return render(request, 'members/signup.html', context)