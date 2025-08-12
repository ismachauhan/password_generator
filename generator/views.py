import qrcode
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import timezone
from django.core.files.base import ContentFile
from .models import Password
import random
import string
from datetime import timedelta

def index(request):
    return render(request, 'generator/index.html')

@login_required
def generate_password(request):
    length = int(request.GET.get('length', 12))  # from GET instead of POST

    characters = ""
    if request.GET.get('uppercase'):
        characters += string.ascii_uppercase
    else:
        characters += string.ascii_lowercase

    if request.GET.get('digits'):
        characters += string.digits

    if request.GET.get('symbols'):
        characters += string.punctuation

    # Default fallback
    if not characters:
        characters = string.ascii_letters + string.digits

    generated_password = ''.join(random.choice(characters) for _ in range(length))

    # Save password
    Password.objects.create(user=request.user, password=generated_password)

    return render(request, 'generator/index.html', {'password': generated_password})


@login_required
def password_history(request):
    passwords = Password.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'generator/history.html', {'passwords': passwords})

@login_required
def toggle_favorite(request, password_id):
    password = get_object_or_404(Password, id=password_id, user=request.user)
    password.is_favorite = not password.is_favorite
    password.save()
    return redirect('password_history')

@login_required
def delete_password(request, password_id):
    password = get_object_or_404(Password, id=password_id, user=request.user)
    password.delete()
    return redirect('password_history')

@login_required
def generate_qr_code(request, password_id):
    password = get_object_or_404(Password, id=password_id, user=request.user)

    # If QR already exists and is still valid, skip regeneration
    if password.qr_code and password.qr_expiry and timezone.now() < password.qr_expiry:
        return redirect('password_history')

    # Generate QR code image
    img = qrcode.make(password.password)
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)  # ✅ Important: reset pointer
    qr_img = ContentFile(buffer.read())

    # Save file into MEDIA_ROOT/qr_codes/
    password.qr_code.save(f'qr_{password.id}.png', qr_img, save=False)
    password.qr_expiry = timezone.now() + timedelta(minutes=10)
    password.is_qr_used = False
    password.save()

    return redirect('password_history')

@login_required
def scan_qr_code(request, password_id):
    password = get_object_or_404(Password, id=password_id)

    if password.qr_expiry and timezone.now() > password.qr_expiry:
        return HttpResponse("QR code expired.")

    if password.is_qr_used:
        return HttpResponse("QR code already used.")

    password.is_qr_used = True
    password.save()

    return HttpResponse(f"Scanned password: {password.password}")
