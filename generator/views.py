import random
import string
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Password


def index(request):
    favorite_passwords = []
    if request.user.is_authenticated:
        favorite_passwords = Password.objects.filter(
            user=request.user, is_favorite=True
        ).values_list('password', flat=True)

    return render(request, 'generator/index.html', {
        'favorite_passwords': favorite_passwords
    })


@login_required
def generate_password(request):
    length = int(request.GET.get('length', 12))

    characters = ""
    if request.GET.get('uppercase'):
        characters += string.ascii_uppercase
    else:
        characters += string.ascii_lowercase

    if request.GET.get('digits'):
        characters += string.digits

    if request.GET.get('symbols'):
        characters += string.punctuation

    if not characters:
        characters = string.ascii_letters + string.digits

    generated_password = ''.join(random.choice(characters) for _ in range(length))

    # Save the password to DB
    password_obj = Password.objects.create(
        user=request.user,
        password=generated_password
    )

    favorite_passwords = Password.objects.filter(
        user=request.user, is_favorite=True
    ).values_list('password', flat=True)

    return render(request, 'generator/index.html', {
        'password': password_obj,  # pass object, not string
        'favorite_passwords': favorite_passwords
    })


@login_required
def toggle_favorite(request, password_id):
    password = get_object_or_404(Password, id=password_id, user=request.user)
    password.is_favorite = not password.is_favorite  # toggles on/off
    password.save()
    return redirect('index')


@login_required
def password_history(request):
    passwords = Password.objects.filter(user=request.user).order_by('-created_at')
    favorite_passwords = Password.objects.filter(
        user=request.user, is_favorite=True
    ).values_list('password', flat=True)

    return render(request, 'generator/password_history.html', {
        'passwords': passwords,
        'favorite_passwords': favorite_passwords
    })


@login_required
def delete_password(request, password_id):
    password = get_object_or_404(Password, id=password_id, user=request.user)
    password.delete()
    return redirect('password_history')

@login_required
def view_favorites(request):
    favorites = Password.objects.filter(user=request.user, is_favorite=True).order_by('-created_at')
    return render(request, 'generator/favorite_passwords.html', {
        'favorites': favorites
    })

