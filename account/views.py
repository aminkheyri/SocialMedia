from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, UserLoginForm, EditProfileForm, PhoneLoginForm, VerifyCodeForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from posts.models import Post
from django.contrib.auth.decorators import login_required
from random import randint
from kavenegar import *
from .models import Profile, Relation
from django.http import JsonResponse

def user_login(request):
    next = request.GET.get('next')
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'Congrats You have logged in', 'success')
                if next:
                    return redirect(next)
                return redirect('posts:all_posts')
            else:
                messages.error(request, 'Your Username or Password is incorrect', 'danger')
    else:
        form = UserLoginForm()
    return render(request, 'account/login.html', {'form': form})


def user_register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(cd['username'], cd['email'], cd['password'])
            login(request, user)
            messages.success(request, 'Congrats You have Registered successfully', 'success')
            return redirect('posts:all_posts')
        else:
            messages.error(request, 'something went wrong ')
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You Logged out successfully', 'success')
    return redirect('posts:all_posts')


@login_required
def user_dashboard(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(user=user)
    self_dash = False
    is_following = False
    relation = Relation.objects.filter(from_user=request.user, to_user=user)
    if relation.exists():
        is_following = True
    if request.user.id == user_id:
        self_dash = True
    return render(request, 'account/dashboard.html', {'user': user, 'posts': posts,
                                                      'self_dash': self_dash, 'is_following': is_following})


@login_required
def edit_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=user.profile)
        if form.is_valid():
            form.save()
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            messages.success(request, 'your profile edited successfully', 'success')
            return redirect('account:dashboard', user_id)
    else:
        form = EditProfileForm(instance=user.profile, initial={'email': request.user.email, 'first_name':
        request.user.first_name, 'last_name': request.user.last_name})

    return render(request, 'account/edit_profile.html', {'form': form})


def phone_login(request):
    if request.method == "POST":
        form = PhoneLoginForm(request.POST)
        if form.is_valid():
            global phone, rand_num
            phone = f"0{form.cleaned_data['phone']}"
            rand_num = randint(1000, 9999)
            api = KavenegarAPI('584D34694977644E474C64776950746533335A524B624F4A77644B314A56766956736366593077693972593D')
            params = {'sender': '', 'receptor': phone, 'message': rand_num}
            api.sms_send(params)
            return redirect('account:verify')
    else:
        form = PhoneLoginForm()
    return render(request, 'account/phone_login.html', {'form': form})


def verify(request):
    if request.method == "POST":
        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            if rand_num == form.cleaned_data['code']:
                profile = get_object_or_404(Profile, phone=phone)
                user = get_object_or_404(User, profile__id=profile.id)
                login(request, user)
                messages.success(request, 'You logged in successfully', 'success')
                return redirect('posts:all_posts')
            else:
                messages.error(request, 'Your Code is Wrong', 'danger')
    else:
        form = VerifyCodeForm()
    return render(request, 'account/verify.html', {'form': form})


@login_required
def follow(request):
    if request.method == "POST":
        user_id = request.POST['user_id']
        following = get_object_or_404(User, pk=user_id)
        check_relation = Relation.objects.filter(from_user=request.user, to_user=following)
        if check_relation.exists():
            return JsonResponse({'status': 'exists'})
        else:
            Relation(from_user=request.user, to_user=following).save()
            return JsonResponse({'status': 'ok'})


@login_required
def unfollow(request):
    if request.method == "POST":
        user_id = request.POST['user_id']
        following = get_object_or_404(User, pk=user_id)
        check_relation = Relation.objects.filter(from_user=request.user, to_user=following)
        if check_relation.exists():
            check_relation.delete()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'notexists'})
