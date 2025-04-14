import re
import socket
from django.core.exceptions import ValidationError

def validate_email_domain(email):
    domain = email.split('@')[-1]
    try:
        socket.gethostbyname(domain)
    except socket.gaierror:
        raise ValidationError(f"Домен {domain} не существует.")

def validate_username(username):
    if not re.match(r'^[\w]{3,30}$', username):
        raise ValidationError("Имя пользователя должно содержать от 3 до 30 символов, буквы, цифры и подчёркивания.")

def validate_password(password):
    if len(password) < 8:
        raise ValidationError("Пароль должен содержать минимум 8 символов.")
    if not re.search(r'[A-Z]', password):
        raise ValidationError("Пароль должен содержать хотя бы одну заглавную букву.")
    if not re.search(r'[a-z]', password):
        raise ValidationError("Пароль должен содержать хотя бы одну строчную букву.")
    if not re.search(r'[0-9]', password):
        raise ValidationError("Пароль должен содержать хотя бы одну цифру.")
    if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        raise ValidationError("Пароль должен содержать хотя бы один специальный символ.")